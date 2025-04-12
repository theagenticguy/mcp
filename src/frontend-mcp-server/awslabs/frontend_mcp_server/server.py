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
    topic: Literal['basic-ui'] = Field(
        ...,
        description='The topic of React documentation to retrieve. Must be one of: basic-ui',
    ),
) -> str:
    """Get specific AWS web application UI setup documentation by topic.

    Parameters:
        topic (Literal["basic-ui"]): The topic of React documentation to retrieve.
          - "basic-ui": Documentation for basic UI setup for an AWS Amplify web application.

    Returns:
        A markdown string containing the requested documentation
    """
    match topic:
        case 'basic-ui':
            return load_markdown_file('basic-ui-setup.md')
        case 'routing':
            return load_markdown_file('routing-implementation.md')
        case 'login':
            return load_markdown_file('login-screen-customization.md')
        case 'auth':
            return load_markdown_file('amplify_authentication-setup.md')
        case _:
            raise ValueError(f'Invalid topic: {topic}. Must be one of: basic-ui, routing, login, auth')


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
