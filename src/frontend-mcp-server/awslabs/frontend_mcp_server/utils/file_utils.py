"""File utility functions for the frontend MCP server."""

from pathlib import Path
from typing import Tuple


def load_markdown_files() -> Tuple[str, str]:
    """Load markdown files from the static/react directory.

    This function reads the content of React-related markdown documentation
    files from the static/react directory.

    Returns:
        Tuple[str, str]: A tuple containing the content of react_router.md
        and optimistic_ui.md files.
    """
    # Find the path to the static/react directory relative to this file
    # Go up two levels from utils/file_utils.py to the frontend_mcp_server directory
    base_dir = Path(__file__).parent.parent
    react_dir = base_dir / 'static' / 'react'

    react_router_path = react_dir / 'react_router.md'
    optimistic_ui_path = react_dir / 'optimistic_ui.md'

    react_router_content = ''
    optimistic_ui_content = ''

    if react_router_path.exists():
        with open(react_router_path, 'r', encoding='utf-8') as f:
            react_router_content = f.read()
    else:
        print(f'Warning: File not found: {react_router_path}')

    if optimistic_ui_path.exists():
        with open(optimistic_ui_path, 'r', encoding='utf-8') as f:
            optimistic_ui_content = f.read()
    else:
        print(f'Warning: File not found: {optimistic_ui_path}')

    return react_router_content, optimistic_ui_content
