# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""DataCatalogHandler for Data Processing MCP Server."""

from awslabs.aws_dataprocessing_mcp_server.core.glue_data_catalog.data_catalog_database_manager import (
    DataCatalogDatabaseManager,
)
from awslabs.aws_dataprocessing_mcp_server.core.glue_data_catalog.data_catalog_handler import (
    DataCatalogManager,
)
from awslabs.aws_dataprocessing_mcp_server.core.glue_data_catalog.data_catalog_table_manager import (
    DataCatalogTableManager,
)
from awslabs.aws_dataprocessing_mcp_server.models.data_catalog_models import (
    CreateCatalogResponse,
    CreateConnectionResponse,
    CreateDatabaseResponse,
    CreatePartitionResponse,
    CreateTableResponse,
    DeleteCatalogResponse,
    DeleteConnectionResponse,
    DeleteDatabaseResponse,
    DeletePartitionResponse,
    DeleteTableResponse,
    GetCatalogResponse,
    GetConnectionResponse,
    GetDatabaseResponse,
    GetPartitionResponse,
    GetTableResponse,
    ImportCatalogResponse,
    ListCatalogsResponse,
    ListConnectionsResponse,
    ListDatabasesResponse,
    ListPartitionsResponse,
    ListTablesResponse,
    SearchTablesResponse,
    UpdateConnectionResponse,
    UpdateDatabaseResponse,
    UpdatePartitionResponse,
    UpdateTableResponse,
)
from awslabs.aws_dataprocessing_mcp_server.utils.logging_helper import (
    LogLevel,
    log_with_request_id,
)
from mcp.server.fastmcp import Context
from mcp.types import TextContent
from pydantic import Field
from typing import Annotated, Any, Dict, List, Optional, Union


class GlueDataCatalogHandler:
    """Handler for Amazon Glue Data Catalog operations."""

    def __init__(self, mcp, allow_write: bool = False, allow_sensitive_data_access: bool = False):
        """Initialize the Glue Data Catalog handler.

        Args:
            mcp: The MCP server instance
            allow_write: Whether to enable write access (default: False)
            allow_sensitive_data_access: Whether to allow access to sensitive data (default: False)
        """
        self.mcp = mcp
        self.allow_write = allow_write
        self.allow_sensitive_data_access = allow_sensitive_data_access
        self.data_catalog_database_manager = DataCatalogDatabaseManager(
            self.allow_write, self.allow_sensitive_data_access
        )
        self.data_catalog_table_manager = DataCatalogTableManager(
            self.allow_write, self.allow_sensitive_data_access
        )
        self.data_catalog_manager = DataCatalogManager(
            self.allow_write, self.allow_sensitive_data_access
        )

        # Register tools
        self.mcp.tool(name='manage_aws_glue_databases')(
            self.manage_aws_glue_data_catalog_databases
        )
        self.mcp.tool(name='manage_aws_glue_tables')(self.manage_aws_glue_data_catalog_tables)
        self.mcp.tool(name='manage_aws_glue_connections')(
            self.manage_aws_glue_data_catalog_connections
        )
        self.mcp.tool(name='manage_aws_glue_partitions')(
            self.manage_aws_glue_data_catalog_partitions
        )
        self.mcp.tool(name='manage_aws_glue_catalog')(self.manage_aws_glue_data_catalog)

    async def manage_aws_glue_data_catalog_databases(
        self,
        ctx: Context,
        operation: Annotated[
            str,
            Field(
                description='Operation to perform: create-database, delete-database, get-database, list-databases, or update-database. Choose "get-database" or "list-databases" for read-only operations when write access is disabled.',
            ),
        ],
        database_name: Annotated[
            Optional[str],
            Field(
                description='Name of the database (required for create-database, delete-database, get-database, and update-database operations).',
            ),
        ] = None,
        description: Annotated[
            Optional[str],
            Field(
                description='Description of the database (for create-database and update-database operations).',
            ),
        ] = None,
        location_uri: Annotated[
            Optional[str],
            Field(
                description='Location URI of the database (for create-database and update-database operations).',
            ),
        ] = None,
        parameters: Annotated[
            Optional[Dict[str, Any]],
            Field(
                description='Key-value pairs that define parameters and properties of the database.',
            ),
        ] = None,
        catalog_id: Annotated[
            Optional[str],
            Field(
                description='ID of the catalog (optional, defaults to account ID).',
            ),
        ] = None,
        max_results: Annotated[
            Optional[int],
            Field(description='The maximum number of databases to return in one response.'),
        ] = None,
        next_token: Annotated[
            Optional[str],
            Field(
                description='A continuation token, if this is a continuation call.',
            ),
        ] = None,
    ) -> Union[
        CreateDatabaseResponse,
        DeleteDatabaseResponse,
        GetDatabaseResponse,
        ListDatabasesResponse,
        UpdateDatabaseResponse,
    ]:
        """Manage AWS Glue Data Catalog databases with both read and write operations.

        This tool provides operations for managing Glue Data Catalog databases, including creating,
        updating, retrieving, listing, and deleting databases. It serves as the primary mechanism
        for database management within the AWS Glue Data Catalog.

        ## Requirements
        - The server must be run with the `--allow-write` flag for create-database, update-database, and delete-database operations
        - Appropriate AWS permissions for Glue Data Catalog operations

        ## Operations
        - **create-database**: Create a new database in the Glue Data Catalog
        - **delete-database**: Delete an existing database from the Glue Data Catalog
        - **get-database**: Retrieve detailed information about a specific database
        - **list-databases**: List all databases in the Glue Data Catalog
        - **update-database**: Update an existing database's properties

        ## Usage Tips
        - Use the get-database or list-databases operations first to check existing databases
        - Database names must be unique within your AWS account and region
        - Deleting a database will also delete all tables within it

        Args:
            ctx: MCP context
            operation: Operation to perform (create-database, delete-database, get-database, list-databases, update-database)
            database_name: Name of the database (required for most operations)
            description: Description of the database
            location_uri: Location URI of the database
            parameters: Additional parameters for the database
            catalog_id: ID of the catalog (optional, defaults to account ID)
            max_results: The maximum number of databases to return in one response.
            next_token: A continuation string token, if this is a continuation call.

        Returns:
            Union of response types specific to the operation performed
        """
        log_with_request_id(
            ctx,
            LogLevel.INFO,
            f'Received request to manage AWS Glue Data Catalog databases with operation: {operation} database_name: {database_name}, description {description}',
        )
        try:
            if not self.allow_write and operation not in [
                'get-database',
                'list-databases',
            ]:
                error_message = f'Operation {operation} is not allowed without write access'
                log_with_request_id(ctx, LogLevel.ERROR, error_message)

                if operation == 'create-database':
                    return CreateDatabaseResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        database_name='',
                        operation='create-database',
                    )
                elif operation == 'delete-database':
                    return DeleteDatabaseResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        database_name='',
                        operation='delete-database',
                    )
                elif operation == 'update-database':
                    return UpdateDatabaseResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        database_name='',
                        operation='update-database',
                    )
                else:
                    return GetDatabaseResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        database_name='',
                        description='',
                        location_uri='',
                        parameters={},
                        creation_time='',
                        operation='get-database',
                        catalog_id='',
                    )

            if operation == 'create-database':
                if database_name is None:
                    raise ValueError('database_name is required for create-database operation')
                return await self.data_catalog_database_manager.create_database(
                    ctx=ctx,
                    database_name=database_name,
                    description=description,
                    location_uri=location_uri,
                    parameters=parameters,
                    catalog_id=catalog_id,
                )

            elif operation == 'delete-database':
                if database_name is None:
                    raise ValueError('database_name is required for delete-database operation')
                return await self.data_catalog_database_manager.delete_database(
                    ctx=ctx, database_name=database_name, catalog_id=catalog_id
                )

            elif operation == 'get-database':
                if database_name is None:
                    raise ValueError('database_name is required for get-database operation')
                return await self.data_catalog_database_manager.get_database(
                    ctx=ctx, database_name=database_name, catalog_id=catalog_id
                )

            elif operation == 'list-databases':
                return await self.data_catalog_database_manager.list_databases(
                    ctx=ctx, catalog_id=catalog_id, next_token=next_token, max_results=max_results
                )

            elif operation == 'update-database':
                if database_name is None:
                    raise ValueError('database_name is required for update-database operation')
                return await self.data_catalog_database_manager.update_database(
                    ctx=ctx,
                    database_name=database_name,
                    description=description,
                    location_uri=location_uri,
                    parameters=parameters,
                    catalog_id=catalog_id,
                )

            else:
                error_message = f'Invalid operation: {operation}. Must be one of: create-database, delete-database, get-database, list-databases, update-database'
                log_with_request_id(ctx, LogLevel.ERROR, error_message)
                return GetDatabaseResponse(
                    isError=True,
                    content=[TextContent(type='text', text=error_message)],
                    database_name='',
                    description='',
                    location_uri='',
                    parameters={},
                    creation_time='',
                    operation='get-database',
                    catalog_id='',
                )

        except ValueError as e:
            log_with_request_id(ctx, LogLevel.ERROR, f'Parameter validation error: {str(e)}')
            raise
        except Exception as e:
            error_message = f'Error in manage_aws_glue_data_catalog_databases: {str(e)}'
            log_with_request_id(ctx, LogLevel.ERROR, error_message)
            # No need to convert catalog_id as we're using empty string directly
            return GetDatabaseResponse(
                isError=True,
                content=[TextContent(type='text', text=error_message)],
                database_name=database_name or '',
                description='',
                location_uri='',
                parameters={},
                creation_time='',
                operation='get-database',
                catalog_id='',  # Always use empty string for catalog_id in error responses
            )

    async def manage_aws_glue_data_catalog_tables(
        self,
        ctx: Context,
        operation: Annotated[
            str,
            Field(
                description='Operation to perform: create-table, delete-table, get-table, list-tables, update-table, or search-tables. Choose "get-table", "list-tables", or "search-tables" for read-only operations.',
            ),
        ],
        database_name: Annotated[
            str,
            Field(
                description='Name of the database containing the table.',
            ),
        ],
        table_name: Annotated[
            Optional[str],
            Field(
                description='Name of the table (required for create-table, delete-table, get-table, and update-table operations).',
            ),
        ] = None,
        catalog_id: Annotated[
            Optional[str],
            Field(
                description='ID of the catalog (optional, defaults to account ID).',
            ),
        ] = None,
        table_input: Annotated[
            Optional[Dict[str, Any]],
            Field(
                description='Table definition for create-table and update-table operations.',
            ),
        ] = None,
        search_text: Annotated[
            Optional[str],
            Field(
                description='Search text for search-tables operation.',
            ),
        ] = None,
        max_results: Annotated[
            Optional[int],
            Field(
                description='Maximum number of results to return for list and search-tables operations.',
            ),
        ] = None,
        next_token: Annotated[
            Optional[str],
            Field(description='A continuation token, included if this is a continuation call.'),
        ] = None,
    ) -> Union[
        CreateTableResponse,
        DeleteTableResponse,
        GetTableResponse,
        ListTablesResponse,
        UpdateTableResponse,
        SearchTablesResponse,
    ]:
        """Manage AWS Glue Data Catalog tables with both read and write operations.

        This tool provides comprehensive operations for managing Glue Data Catalog tables,
        including creating, updating, retrieving, listing, searching, and deleting tables.
        Tables define the schema and metadata for data stored in various formats and locations.

        ## Requirements
        - The server must be run with the `--allow-write` flag for create-table, update-table, and delete-table operations
        - Database must exist before creating tables within it
        - Appropriate AWS permissions for Glue Data Catalog operations

        ## Operations
        - **create-table**: Create a new table in the specified database
        - **delete-table**: Delete an existing table from the database
        - **get-table**: Retrieve detailed information about a specific table
        - **list-tables**: List all tables in the specified database
        - **update-table**: Update an existing table's properties
        - **search-tables**: Search for tables using text matching

        ## Usage Tips
        - Table names must be unique within a database
        - Use get-table or list-tables operations to check existing tables before creating
        - Table input should include storage descriptor, columns, and partitioning information

        Args:
            ctx: MCP context
            operation: Operation to perform
            database_name: Name of the database
            table_name: Name of the table
            catalog_id: ID of the catalog (optional, defaults to account ID)
            table_input: Table definition
            search_text: Search text for search operation
            max_results: Maximum results to return
            next_token: A continuation string token, if this is a continuation call

        Returns:
            Union of response types specific to the operation performed
        """
        if operation not in [
            'create-table',
            'delete-table',
            'get-table',
            'list-tables',
            'update-table',
            'search-tables',
        ]:
            error_message = f'Invalid operation: {operation}. Must be one of: create-table, delete-table, get-table, list-tables, update-table, search-tables'
            log_with_request_id(ctx, LogLevel.ERROR, error_message)
            return GetTableResponse(
                isError=True,
                content=[TextContent(type='text', text=error_message)],
                database_name=database_name,
                table_name='',
                table_definition={},
                creation_time='',
                last_access_time='',
                operation='get-table',
            )

        try:
            if not self.allow_write and operation not in [
                'get-table',
                'list-tables',
                'search-tables',
            ]:
                error_message = f'Operation {operation} is not allowed without write access'
                log_with_request_id(ctx, LogLevel.ERROR, error_message)

                if operation == 'create-table':
                    return CreateTableResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        database_name=database_name,
                        table_name='',
                        operation='create-table',
                    )
                elif operation == 'delete-table':
                    return DeleteTableResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        database_name=database_name,
                        table_name='',
                        operation='delete-table',
                    )
                elif operation == 'update-table':
                    return UpdateTableResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        database_name=database_name,
                        table_name='',
                        operation='update-table',
                    )
                elif operation == 'search-tables':
                    return SearchTablesResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        tables=[],
                        search_text='',
                        count=0,
                        operation='search-tables',
                    )
                else:
                    return GetTableResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        database_name=database_name,
                        table_name='',
                        table_definition={},
                        creation_time='',
                        last_access_time='',
                        operation='get-table',
                    )

            if operation == 'create-table':
                if database_name is None or table_input is None or table_name is None:
                    raise ValueError(
                        'database_name, table_input and table_name are required for create-table operation'
                    )
                return await self.data_catalog_table_manager.create_table(
                    ctx=ctx,
                    database_name=database_name,
                    table_name=table_name,
                    table_input=table_input,
                    catalog_id=catalog_id,
                )

            elif operation == 'delete-table':
                if table_name is None or database_name is None:
                    raise ValueError(
                        'table_name and database_name required for delete-table operation'
                    )
                return await self.data_catalog_table_manager.delete_table(
                    ctx=ctx,
                    database_name=database_name,
                    table_name=table_name,
                    catalog_id=catalog_id,
                )

            elif operation == 'get-table':
                if table_name is None:
                    raise ValueError('table_name is required for get-table operation')
                return await self.data_catalog_table_manager.get_table(
                    ctx=ctx,
                    database_name=database_name,
                    table_name=table_name,
                    catalog_id=catalog_id,
                )

            elif operation == 'list-tables':
                return await self.data_catalog_table_manager.list_tables(
                    ctx=ctx,
                    database_name=database_name,
                    max_results=max_results,
                    catalog_id=catalog_id,
                    next_token=next_token,
                )

            elif operation == 'update-table':
                if table_name is None or table_input is None:
                    raise ValueError(
                        'table_name and table_input are required for update-table operation'
                    )
                return await self.data_catalog_table_manager.update_table(
                    ctx=ctx,
                    database_name=database_name,
                    table_name=table_name,
                    table_input=table_input,
                    catalog_id=catalog_id,
                )

            elif operation == 'search-tables':
                return await self.data_catalog_table_manager.search_tables(
                    ctx=ctx,
                    search_text=search_text,
                    max_results=max_results,
                    catalog_id=catalog_id,
                )
            else:
                error_message = f'Invalid operation: {operation}. Must be one of: create-table, delete-table, get-table, list-tables, update-table, search-tables'
                log_with_request_id(ctx, LogLevel.ERROR, error_message)
                return GetTableResponse(
                    isError=True,
                    content=[TextContent(type='text', text=error_message)],
                    database_name=database_name,
                    table_name='',
                    table_definition={},
                    creation_time='',
                    last_access_time='',
                    operation='get-table',
                )

        except ValueError as e:
            log_with_request_id(ctx, LogLevel.ERROR, f'Parameter validation error: {str(e)}')
            raise
        except Exception as e:
            error_message = f'Error in manage_aws_glue_data_catalog_tables: {str(e)}'
            log_with_request_id(ctx, LogLevel.ERROR, error_message)
            return GetTableResponse(
                isError=True,
                content=[TextContent(type='text', text=error_message)],
                database_name=database_name,
                table_name='',  # Always use empty string for table_name in error responses
                table_definition={},
                creation_time='',
                last_access_time='',
                operation='get-table',
            )

    async def manage_aws_glue_data_catalog_connections(
        self,
        ctx: Context,
        operation: Annotated[
            str,
            Field(
                description='Operation to perform: create-connection, delete-connection, get-connection, list-connections, or update-connection. Choose "get-connection" or "list-connections" for read-only operations.',
            ),
        ],
        connection_name: Annotated[
            Optional[str],
            Field(
                description='Name of the connection (required for create-connection, delete-connection, get-connection, and update-connection operations).',
            ),
        ] = None,
        connection_input: Annotated[
            Optional[Dict[str, Any]],
            Field(
                description='Connection definition for create and update operations.',
            ),
        ] = None,
        catalog_id: Annotated[
            Optional[str],
            Field(
                description='Catalog ID for the connection (optional, defaults to account ID).',
            ),
        ] = None,
        max_results: Annotated[
            Optional[int],
            Field(description='The maximum number of connections to return in one response.'),
        ] = None,
        next_token: Annotated[
            Optional[str],
            Field(description='A continuation token, if this is a continuation call.'),
        ] = None,
        hide_password: Annotated[
            Optional[bool],
            Field(
                description='Flag to retrieve the connection metadata without returning the password(for get-connection and list-connections operation).',
            ),
        ] = True,
    ) -> Union[
        CreateConnectionResponse,
        DeleteConnectionResponse,
        GetConnectionResponse,
        ListConnectionsResponse,
        UpdateConnectionResponse,
    ]:
        """Manage AWS Glue Data Catalog connections with both read and write operations.

        Connections in AWS Glue store connection information for data stores,
        such as databases, data warehouses, and other data sources. They contain
        connection properties like JDBC URLs, usernames, and other metadata needed
        to connect to external data sources.

        ## Requirements
        - The server must be run with the `--allow-write` flag for create, update, and delete operations
        - Appropriate AWS permissions for Glue Data Catalog operations
        - Connection properties must be valid for the connection type

        ## Operations
        - **create-connection**: Create a new connection
        - **delete-connection**: Delete an existing connection
        - **get-connection**: Retrieve detailed information about a specific connection
        - **list-connections**: List all connections
        - **update-connection**: Update an existing connection's properties

        ## Usage Tips
        - Connection names must be unique within your catalog
        - Connection input should include ConnectionType and ConnectionProperties
        - Use get or list operations to check existing connections before creating

        Args:
            ctx: MCP context
            operation: Operation to perform
            connection_name: Name of the connection
            connection_input: Connection definition
            catalog_id: Catalog ID for the connection
            max_results: Maximum results to return
            next_token: A continuation string token, if this is a continuation call
            hide_password: The boolean flag to control connection password in return value for get-connection and list-connections operation

        Returns:
            Union of response types specific to the operation performed
        """
        if operation not in [
            'create-connection',
            'delete-connection',
            'get-connection',
            'list-connections',
            'update-connection',
        ]:
            error_message = f'Invalid operation: {operation}. Must be one of: create-connection, delete-connection, get-connection, list-connections, update-connection'
            log_with_request_id(ctx, LogLevel.ERROR, error_message)
            return GetConnectionResponse(
                isError=True,
                content=[TextContent(type='text', text=error_message)],
                connection_name='',
                connection_type='',
                connection_properties={},
                physical_connection_requirements=None,
                creation_time='',
                last_updated_time='',
                last_updated_by='',
                status='',
                status_reason='',
                last_connection_validation_time='',
                catalog_id='',
                operation='get-connection',
            )

        try:
            if not self.allow_write and operation not in [
                'get-connection',
                'list-connections',
            ]:
                error_message = f'Operation {operation} is not allowed without write access'
                log_with_request_id(ctx, LogLevel.ERROR, error_message)

                if operation == 'create-connection':
                    return CreateConnectionResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        connection_name='',
                        operation='create-connection',
                        catalog_id='',
                    )
                elif operation == 'delete-connection':
                    return DeleteConnectionResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        connection_name='',
                        operation='delete-connection',
                        catalog_id='',
                    )
                elif operation == 'update-connection':
                    return UpdateConnectionResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        connection_name='',
                        operation='update-connection',
                        catalog_id='',
                    )
                else:
                    return GetConnectionResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        connection_name='',
                        connection_type='',
                        connection_properties={},
                        physical_connection_requirements=None,
                        creation_time='',
                        last_updated_time='',
                        last_updated_by='',
                        status='',
                        status_reason='',
                        last_connection_validation_time='',
                        catalog_id='',
                        operation='get',
                    )

            if operation == 'create-connection':
                if connection_name is None or connection_input is None:
                    raise ValueError(
                        'connection_name and connection_input are required for create operation'
                    )
                return await self.data_catalog_manager.create_connection(
                    ctx=ctx,
                    connection_name=connection_name,
                    connection_input=connection_input,
                    catalog_id=catalog_id,
                )

            elif operation == 'delete-connection':
                if connection_name is None:
                    raise ValueError('connection_name is required for delete operation')
                return await self.data_catalog_manager.delete_connection(
                    ctx=ctx, connection_name=connection_name, catalog_id=catalog_id
                )

            elif operation == 'get-connection':
                if connection_name is None:
                    raise ValueError('connection_name is required for get operation')
                return await self.data_catalog_manager.get_connection(
                    ctx=ctx,
                    connection_name=connection_name,
                    catalog_id=catalog_id,
                    hide_password=hide_password,
                )

            elif operation == 'list-connections':
                return await self.data_catalog_manager.list_connections(
                    ctx=ctx,
                    catalog_id=catalog_id,
                    max_results=max_results,
                    next_token=next_token,
                    hide_password=hide_password,
                )

            elif operation == 'update-connection':
                if connection_name is None or connection_input is None:
                    raise ValueError(
                        'connection_name and connection_input are required for update operation'
                    )
                return await self.data_catalog_manager.update_connection(
                    ctx=ctx,
                    connection_name=connection_name,
                    connection_input=connection_input,
                    catalog_id=catalog_id,
                )
            else:
                error_message = f'Invalid operation: {operation}. Must be one of: create-connection, delete-connection, get-connection, list-connections, update-connection'
                log_with_request_id(ctx, LogLevel.ERROR, error_message)
                return GetConnectionResponse(
                    isError=True,
                    content=[TextContent(type='text', text=error_message)],
                    connection_name='',
                    connection_type='',
                    connection_properties={},
                    physical_connection_requirements=None,
                    creation_time='',
                    last_updated_time='',
                    last_updated_by='',
                    status='',
                    status_reason='',
                    last_connection_validation_time='',
                    catalog_id='',
                    operation='get-connection',
                )

        except ValueError as e:
            log_with_request_id(ctx, LogLevel.ERROR, f'Parameter validation error: {str(e)}')
            raise
        except Exception as e:
            error_message = f'Error in manage_aws_glue_data_catalog_connections: {str(e)}'
            log_with_request_id(ctx, LogLevel.ERROR, error_message)
            return GetConnectionResponse(
                isError=True,
                content=[TextContent(type='text', text=error_message)],
                connection_name='',  # Always use empty string for connection_name in error responses
                connection_type='',
                connection_properties={},
                physical_connection_requirements=None,
                creation_time='',
                last_updated_time='',
                last_updated_by='',
                status='',
                status_reason='',
                last_connection_validation_time='',
                catalog_id='',  # Always use empty string for catalog_id in error responses
                operation='get-connection',
            )

    async def manage_aws_glue_data_catalog_partitions(
        self,
        ctx: Context,
        operation: Annotated[
            str,
            Field(
                description='Operation to perform: create-partition, delete-partition, get-partition, list-partitions, or update-partition. Choose "get-partition" or "list-partitions" for read-only operations.',
            ),
        ],
        database_name: Annotated[
            str,
            Field(
                description='Name of the database containing the table.',
            ),
        ],
        table_name: Annotated[
            str,
            Field(
                description='Name of the table containing the partition.',
            ),
        ],
        partition_values: Annotated[
            Optional[List[str]],
            Field(
                description='Values that define the partition (required for create-partition, delete-partition, get-partition, and update-partition operations).',
            ),
        ] = None,
        partition_input: Annotated[
            Optional[Dict[str, Any]],
            Field(
                description='Partition definition for create-partition and update-partition operations.',
            ),
        ] = None,
        max_results: Annotated[
            Optional[int],
            Field(
                description='Maximum number of results to return for list-partitions operation.',
            ),
        ] = None,
        next_token: Annotated[
            Optional[str],
            Field(
                description='A continuation token, if this is not the first call to retrieve these partitions.',
            ),
        ] = None,
        expression: Annotated[
            Optional[str],
            Field(
                description='Filter expression for list-partitions operation.',
            ),
        ] = None,
        catalog_id: Annotated[
            Optional[str],
            Field(
                description='ID of the catalog (optional, defaults to account ID).',
            ),
        ] = None,
    ) -> Union[
        CreatePartitionResponse,
        DeletePartitionResponse,
        GetPartitionResponse,
        ListPartitionsResponse,
        UpdatePartitionResponse,
    ]:
        """Manage AWS Glue Data Catalog partitions with both read and write operations.

        Partitions in AWS Glue represent a way to organize table data based on the values
        of one or more columns. They enable efficient querying and processing of large datasets
        by allowing queries to target specific subsets of data.

        ## Requirements
        - The server must be run with the `--allow-write` flag for create-partition, update-partition, and delete-partition operations
        - Database and table must exist before creating partitions
        - Partition values must match the partition schema defined in the table

        ## Operations
        - **create-partition**: Create a new partition in the specified table
        - **delete-partition**: Delete an existing partition from the table
        - **get-partition**: Retrieve detailed information about a specific partition
        - **list-partitions**: List all partitions in the specified table
        - **update-partition**: Update an existing partition's properties

        ## Usage Tips
        - Partition values must be provided in the same order as partition columns in the table
        - Use get-partition or list-partitions operations to check existing partitions before creating
        - Partition input should include storage descriptor and location information

        Args:
            ctx: MCP context
            operation: Operation to perform
            database_name: Name of the database
            table_name: Name of the table
            partition_values: Values that define the partition
            partition_input: Partition definition
            max_results: Maximum results to return
            next_token: A continuation token, if this is not the first call to retrieve these partitions
            expression: Filter expression for list-partitions operation
            catalog_id: ID of the catalog (optional, defaults to account ID)

        Returns:
            Union of response types specific to the operation performed
        """
        if operation not in [
            'create-partition',
            'delete-partition',
            'get-partition',
            'list-partitions',
            'update-partition',
        ]:
            error_message = f'Invalid operation: {operation}. Must be one of: create-partition, delete-partition, get-partition, list-partitions, update-partition'
            log_with_request_id(ctx, LogLevel.ERROR, error_message)
            return GetPartitionResponse(
                isError=True,
                content=[TextContent(type='text', text=error_message)],
                database_name=database_name,
                table_name=table_name,
                partition_values=[],
                partition_definition={},
                creation_time='',
                last_access_time='',
                operation='get-partition',
            )
        try:
            if not self.allow_write and operation not in [
                'get-partition',
                'list-partitions',
            ]:
                error_message = f'Operation {operation} is not allowed without write access'
                log_with_request_id(ctx, LogLevel.ERROR, error_message)

                if operation == 'create-partition':
                    return CreatePartitionResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        database_name=database_name,
                        table_name=table_name,
                        partition_values=[],
                        operation='create-partition',
                    )
                elif operation == 'delete-partition':
                    return DeletePartitionResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        database_name=database_name,
                        table_name=table_name,
                        partition_values=[],
                        operation='delete-partition',
                    )
                elif operation == 'update-partition':
                    return UpdatePartitionResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        database_name=database_name,
                        table_name=table_name,
                        partition_values=[],
                        operation='update-partition',
                    )
                else:
                    return GetPartitionResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        database_name=database_name,
                        table_name=table_name,
                        partition_values=[],
                        partition_definition={},
                        creation_time='',
                        last_access_time='',
                        operation='get-partition',
                    )

            if operation == 'create-partition':
                if partition_values is None or partition_input is None:
                    raise ValueError(
                        'partition_values and partition_input are required for create-partition operation'
                    )
                return await self.data_catalog_manager.create_partition(
                    ctx=ctx,
                    database_name=database_name,
                    table_name=table_name,
                    partition_values=partition_values,
                    partition_input=partition_input,
                    catalog_id=catalog_id,
                )

            elif operation == 'delete-partition':
                if partition_values is None:
                    raise ValueError('partition_values is required for delete-partition operation')
                return await self.data_catalog_manager.delete_partition(
                    ctx=ctx,
                    database_name=database_name,
                    table_name=table_name,
                    partition_values=partition_values,
                    catalog_id=catalog_id,
                )

            elif operation == 'get-partition':
                if partition_values is None:
                    raise ValueError('partition_values is required for get-partition operation')
                return await self.data_catalog_manager.get_partition(
                    ctx=ctx,
                    database_name=database_name,
                    table_name=table_name,
                    partition_values=partition_values,
                    catalog_id=catalog_id,
                )

            elif operation == 'list-partitions':
                return await self.data_catalog_manager.list_partitions(
                    ctx=ctx,
                    database_name=database_name,
                    table_name=table_name,
                    max_results=max_results,
                    expression=expression,
                    catalog_id=catalog_id,
                    next_token=next_token,
                )

            elif operation == 'update-partition':
                if partition_values is None or partition_input is None:
                    raise ValueError(
                        'partition_values and partition_input are required for update-partition operation'
                    )
                return await self.data_catalog_manager.update_partition(
                    ctx=ctx,
                    database_name=database_name,
                    table_name=table_name,
                    partition_values=partition_values,
                    partition_input=partition_input,
                    catalog_id=catalog_id,
                )
            else:
                error_message = f'Invalid operation: {operation}. Must be one of: create-partition, delete-partition, get-partition, list-partitions, update-partition'
                log_with_request_id(ctx, LogLevel.ERROR, error_message)
                return GetPartitionResponse(
                    isError=True,
                    content=[TextContent(type='text', text=error_message)],
                    database_name=database_name,
                    table_name=table_name,
                    partition_values=[],
                    partition_definition={},
                    creation_time='',
                    last_access_time='',
                    operation='get-partition',
                )

        except ValueError as e:
            log_with_request_id(ctx, LogLevel.ERROR, f'Parameter validation error: {str(e)}')
            raise
        except Exception as e:
            error_message = f'Error in manage_aws_glue_data_catalog_partitions: {str(e)}'
            log_with_request_id(ctx, LogLevel.ERROR, error_message)
            return GetPartitionResponse(
                isError=True,
                content=[TextContent(type='text', text=error_message)],
                database_name=database_name,
                table_name=table_name,
                partition_values=[],  # Always use empty list for partition_values in error responses
                partition_definition={},
                creation_time='',
                last_access_time='',
                operation='get-partition',
            )

    async def manage_aws_glue_data_catalog(
        self,
        ctx: Context,
        operation: Annotated[
            str,
            Field(
                description='Operation to perform: create-catalog, delete-catalog, get-catalog, list-catalogs, or import-catalog-to-glue. Choose "get-catalog" or "list-catalogs" for read-only operations.',
            ),
        ],
        catalog_id: Annotated[
            Optional[str],
            Field(
                description='ID of the catalog (required for create-catalog, delete-catalog, get-catalog, and import-catalog-to-glue operations).',
            ),
        ] = None,
        catalog_input: Annotated[
            Optional[Dict[str, Any]],
            Field(
                description='Catalog definition for create-catalog operations.',
            ),
        ] = None,
        max_results: Annotated[
            Optional[int],
            Field(description='The maximum number of catalogs to return in one response.'),
        ] = None,
        next_token: Annotated[
            Optional[str],
            Field(description='A continuation token, if this is a continuation call.'),
        ] = None,
        parent_catalog_id: Annotated[
            Optional[str],
            Field(
                description='The ID of the parent catalog in which the catalog resides. If none is provided, the AWS Account Number is used by default.',
            ),
        ] = None,
    ) -> Union[
        CreateCatalogResponse,
        DeleteCatalogResponse,
        GetCatalogResponse,
        ListCatalogsResponse,
        ImportCatalogResponse,
    ]:
        """Manage AWS Glue Data Catalog with both read and write operations.

        This tool provides operations for managing the Glue Data Catalog itself,
        including creating custom catalogs, importing from external sources,
        and managing catalog-level configurations.

        ## Requirements
        - The server must be run with the `--allow-write` flag for create-catalog, delete-catalog, and import operations
        - Appropriate AWS permissions for Glue Data Catalog operations
        - For import operations, access to the external data source is required

        ## Operations
        - **create-catalog**: Create a new data catalog
        - **delete-catalog**: Delete an existing data catalog
        - **get-catalog**: Retrieve detailed information about a specific catalog
        - **list-catalogs**: List all available catalogs
        - **import-catalog-to-glue**: Import metadata from external sources into Glue Data Catalog

        ## Usage Tips
        - The default catalog ID is your AWS account ID
        - Custom catalogs allow for better organization and access control
        - Import operations can take significant time depending on source size

        Args:
            ctx: MCP context
            operation: Operation to perform
            catalog_id: ID of the catalog
            catalog_input: Catalog definition
            max_results: The maximum number of catalogs to return in one response
            next_token: A continuation token, if this is a continuation call.
            parent_catalog_id: The ID of the parent catalog in which the catalog resides

        Returns:
            Union of response types specific to the operation performed
        """
        if operation not in [
            'create-catalog',
            'delete-catalog',
            'get-catalog',
            'list-catalogs',
            'import-catalog-to-glue',
        ]:
            error_message = f'Invalid operation: {operation}. Must be one of: create-catalog, delete-catalog, get-catalog, list-catalogs, import-catalog-to-glue'
            log_with_request_id(ctx, LogLevel.ERROR, error_message)
            return GetCatalogResponse(
                isError=True,
                content=[TextContent(type='text', text=error_message)],
                catalog_id='',
                catalog_definition={},
                name='',
                description='',
                create_time='',
                update_time='',
                operation='get-catalog',
            )

        try:
            if not self.allow_write and operation not in [
                'get-catalog',
                'list-catalogs',
            ]:
                error_message = f'Operation {operation} is not allowed without write access'
                log_with_request_id(ctx, LogLevel.ERROR, error_message)

                if operation == 'create-catalog':
                    return CreateCatalogResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        catalog_id='',
                        operation='create-catalog',
                    )
                elif operation == 'delete-catalog':
                    return DeleteCatalogResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        catalog_id='',
                        operation='delete-catalog',
                    )
                elif operation == 'import-catalog-to-glue':
                    return ImportCatalogResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        catalog_id='',
                        operation='import-catalog-to-glue',
                    )
                else:
                    return GetCatalogResponse(
                        isError=True,
                        content=[TextContent(type='text', text=error_message)],
                        catalog_id='',
                        catalog_definition={},
                        name='',
                        description='',
                        create_time='',
                        update_time='',
                        operation='get-catalog',
                    )

            if operation == 'create-catalog':
                if catalog_id is None or catalog_input is None:
                    raise ValueError(
                        'catalog_id and catalog_input are required for create-catalog operation'
                    )
                return await self.data_catalog_manager.create_catalog(
                    ctx=ctx, catalog_name=catalog_id, catalog_input=catalog_input
                )

            elif operation == 'delete-catalog':
                if catalog_id is None:
                    raise ValueError('catalog_id is required for delete-catalog operation')
                return await self.data_catalog_manager.delete_catalog(
                    ctx=ctx, catalog_id=catalog_id
                )

            elif operation == 'get-catalog':
                if catalog_id is None:
                    raise ValueError('catalog_id is required for get-catalog operation')
                return await self.data_catalog_manager.get_catalog(ctx=ctx, catalog_id=catalog_id)

            elif operation == 'list-catalogs':
                return await self.data_catalog_manager.list_catalogs(
                    ctx=ctx,
                    max_results=max_results,
                    next_token=next_token,
                    parent_catalog_id=parent_catalog_id,
                )

            elif operation == 'import-catalog-to-glue':
                if catalog_id is None:
                    raise ValueError('catalog_id is required for import-catalog-to-glue operation')
                return await self.data_catalog_manager.import_catalog_to_glue(
                    ctx=ctx,
                    catalog_id=catalog_id,
                )
            else:
                error_message = f'Invalid operation: {operation}. Must be one of: create-catalog, delete-catalog, get-catalog, list-catalogs, import-catalog-to-glue'
                log_with_request_id(ctx, LogLevel.ERROR, error_message)
                return GetCatalogResponse(
                    isError=True,
                    content=[TextContent(type='text', text=error_message)],
                    catalog_id='',
                    catalog_definition={},
                    name='',
                    description='',
                    create_time='',
                    update_time='',
                    operation='get-catalog',
                )

        except ValueError as e:
            log_with_request_id(ctx, LogLevel.ERROR, f'Parameter validation error: {str(e)}')
            raise
        except Exception as e:
            error_message = f'Error in manage_aws_glue_data_catalog: {str(e)}'
            log_with_request_id(ctx, LogLevel.ERROR, error_message)
            return GetCatalogResponse(
                isError=True,
                content=[TextContent(type='text', text=error_message)],
                catalog_id=catalog_id or '',
                catalog_definition={},
                name='',
                description='',
                create_time='',
                update_time='',
                operation='get-catalog',
            )
