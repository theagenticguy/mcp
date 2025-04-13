"""awslabs frontend MCP Server implementation."""

import argparse
from awslabs.frontend_mcp_server.utils.file_utils import load_markdown_file
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from typing import Literal


mcp = FastMCP(
    'awslabs.frontend-mcp-server',
    instructions="Instructions for using this MCP server. This can be used by clients to improve the LLM's understanding of available tools, resources, etc. It can be thought of like a 'hint' to the model. For example, this information MAY be added to the system prompt. Important to be clear, direct, and detailed.",
    dependencies=[
        'pydantic',
    ],
)


@mcp.tool(name='GetReactDocsByTopic')
async def get_react_docs_by_topic(
    topic: Literal['essential-knowledge', 'basic-ui', 'authentication', 'routing', 'customizing', 'creating-components'] = Field(
        ...,
        description='The topic of React documentation to retrieve. Must be one of: essential-knowledge, basic-ui, authentication, routing, customizing, creating-components. Topics are numbered in recommended sequence.',
    ),
) -> str:
    """Get specific AWS web application UI setup documentation by topic.

    Parameters:
        topic (Literal["essential-knowledge", "basic-ui", "authentication", "routing", "customizing", "creating-components"]): The topic of React documentation to retrieve.
          - 1. "essential-knowledge": Essential knowledge for working with React applications.
          - 2. "basic-ui": Documentation for basic UI setup for an AWS Amplify web application.
          - 3. "authentication": Documentation for setting up authentication in the application.
          - 4. "routing": Documentation for implementing routing in the application.
          - 5. "customizing": Documentation for customizing the application.
          - 6. "creating-components": Documentation for creating new components.

    Returns:
        A markdown string containing the requested documentation
    """
    match topic:
        case 'essential-knowledge':
            return load_markdown_file('essential-knowledge.md')
        case 'basic-ui':
            return load_markdown_file('basic-ui-setup.md')
        case 'authentication':
            return load_markdown_file('authentication-setup.md')
        case 'routing':
            return load_markdown_file('routing-setup.md')
        case 'customizing':
            return load_markdown_file('customizing-the-application.md')
        case 'creating-components':
            return load_markdown_file('creating-components.md')
        case _:
            raise ValueError(f'Invalid topic: {topic}. Must be one of: essential-knowledge, basic-ui, authentication, routing, customizing, creating-components')


def main():
    """Run the MCP server with CLI argument support."""
    parser = argparse.ArgumentParser(
        description='An AWS Labs Model Context Protocol (MCP) server for frontend'
    )
    parser.add_argument('--sse', action='store_true', help='Use SSE transport')
    parser.add_argument('--port', type=int, default=8888, help='Port to run the server on')

    args = parser.parse_args()

    # Run server with appropriate transport
    if args.sse:
        mcp.settings.port = args.port
        mcp.run(transport='sse')
    else:
        mcp.run()


if __name__ == '__main__':
    main()
