"""Command line interface."""

import argparse
import asyncio
import sys
from pathlib import Path

from archive_md_urls.update_files import update_files


def get_md_files(items: list[Path], recursive: bool) -> list[Path]:
    """Scan files and directories and create a list of Markdown files.

    For single file just check if file exists and has the correct file ending (.md).
    For directory, glob for files with .md ending and add each to file list.

    Args:
        item_list (list[str]): List of items provided via argparse
        recursive (bool): Recursively search subdirectories for Markdown files if True

    Returns:
        list[Path]: List of Markdown files to update
    """
    files: list[Path] = []
    for item in items:
        if item.is_dir():
            if recursive:
                files.extend(
                    list(item.rglob("**/*.md"))
                )
            else:
                files.extend(
                    list(item.glob("*.md"))
                )
        elif item.is_file():
            if item.suffix == ".md":
                files.append(item)
            else:
                sys.exit(f"No Markdown file extension (.md): {item}")
        else:
            sys.exit(f"Not a file or directory: {item}.")
    if not files:
        sys.exit("Couldn't find any Markdown files. Do you use the file ending .md for "
                 "your Markdown files? If yes, you could try to search directories "
                 "recursively using the -r flag (see help).")
    return files


def parse_args() -> argparse.Namespace:
    """Parse arguments."""
    argparser = argparse.ArgumentParser(
        description="Turn URLs in Markdown files into Wayback Machine snapshots."
    )
    argparser.add_argument(
        "items",
        nargs='+',
        type=Path,
        help="Markdown file, or directory containing Markdown files. You can specify "
             "multiple items and combine individual files with directories"
    )
    argparser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursively search for Markdown files in subdirectories"
    )
    return argparser.parse_args()


def main() -> None:
    """archive-md-urls cli entry point."""
    args: argparse.Namespace = parse_args()
    files: list[Path] = get_md_files(args.items, args.recursive)
    asyncio.run(update_files(files))


if __name__ == "__main__":
    main()
