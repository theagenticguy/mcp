"""File utility functions for the frontend MCP server."""

from pathlib import Path
from typing import Tuple


def load_markdown_file(filename: str) -> str:
    """Load a markdown file from the static/react directory.

    Args:
        filename (str): The name of the markdown file to load (e.g. 'basic-ui-setup.md')

    Returns:
        str: The content of the markdown file, or empty string if file not found
    """
    base_dir = Path(__file__).parent.parent
    react_dir = base_dir / 'static' / 'react'
    file_path = react_dir / filename

    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print(f'Warning: File not found: {file_path}')
        return ''


def load_markdown_files() -> Tuple[str, str, str, str]:
    """Load all markdown files from the static/react directory.

    Returns:
        Tuple[str, str, str, str]: A tuple containing the content of:
        - basic-ui-setup.md
        - routing-implementation.md
        - login-screen-customization.md
        - amplify_authentication-setup.md
    """
    return (
        load_markdown_file('basic-ui-setup.md'),
        load_markdown_file('routing-implementation.md'),
        load_markdown_file('login-screen-customization.md'),
        load_markdown_file('amplify_authentication-setup.md')
    )
