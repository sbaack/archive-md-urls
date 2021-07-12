"""Turn URLs in Markdown files to Wayback snapshots."""

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
        # Call API and collect snapshots
        wayback_urls: dict[str, Optional[str]] = await get_snapshots(md_source, file)
        # Update links in file source and write file
        updated_md_source: str = update_md_source(md_source, wayback_urls)
        file.write_text(updated_md_source, encoding="utf-8")
        changed_urls += len([item for item in wayback_urls.values() if item])
    print(f"Changed {changed_urls} {'URL' if changed_urls == 1 else 'URLs'} "
          f"in {len(files)} {'file' if len(files) == 1 else 'files'}.")


async def get_snapshots(md_source: str, md_file: Path) -> dict[str, Optional[str]]:
    """Scan Markdown file and call Wayback Machine API to create list of url-snapshot pairs.

    Args:
        md_source (str): Contents of the Markdown file
        md_file (Path): Path of Markdown file

    Returns:
        dict[str, Optional[str]]: API call results with original URL as keys and Wayback
                                  snapshot URLs as values
    """
    date, urls = scan_md(md_source, md_file)
    return await gather_snapshots(urls, date)


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
            md_source = md_source.replace(url, snapshot)
    return md_source
