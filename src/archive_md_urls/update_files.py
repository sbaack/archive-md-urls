"""Turn URLs in Markdown files to Wayback snapshots."""

import re
from pathlib import Path
from typing import Optional

from archive_md_urls.gather_snapshots import gather_snapshots
from archive_md_urls.scan_md import scan_md


async def update_files(files: list[Path]) -> None:
    """Scan and update URLs in Markdown files.

    File contents are updated in-place.

    Args:
        files (list[Path]): List of Markdown files to scan and update
    """
    # Keep count of changed URLs to summarize changes to user
    changed_urls: int = 0
    for file in files:
        md_source: str = file.read_text(encoding="utf-8")
        date, urls = scan_md(md_source, file)
        # Call API and collect snapshots
        wayback_urls: dict[str, Optional[str]] = await gather_snapshots(urls, date)
        # Update links in file source and write file
        updated_md_source: str = update_md_source(md_source, wayback_urls)
        file.write_text(updated_md_source, encoding="utf-8")
        changed_urls += len([item for item in wayback_urls.values() if item])
    print(f"Changed {changed_urls} {'URL' if changed_urls == 1 else 'URLs'} "
          f"in {len(files)} {'file' if len(files) == 1 else 'files'}.")


def update_md_source(md_source: str, wayback_urls: dict[str, Optional[str]]) -> str:
    """Replace URLs in Markdown file with Wayback Snapshots.

    Args:
        md_source (str): Content of Markdown file that should be updated
        wayback_urls (dict[str, Optional[str]]): URL-Snapshot pairs

    Returns:
        str: Content of Markdown file with updated URLs
    """
    for url, snapshot in wayback_urls.items():
        # Skip cases where no Wayback Snapshot was found
        if snapshot:
            # Only replace strings which are == url if they are preceded and
            # followed by braces to avoid mismatches
            md_source = re.sub(fr"(?<=\(){url}(?=\))", snapshot, md_source)
    return md_source
