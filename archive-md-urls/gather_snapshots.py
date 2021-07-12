"""Take URL and return URL of archive.org snapshot.

Given a URL and (optionally) a timestamp, return the URL of the archive.org
snapshot closest to the provided timestamp. If no timestamp is provided or no
snapshot for the provided timestamp cannot be found, return the latest
snapshot. If no snapshot available, return None.
"""

import asyncio
import sys
from typing import Any, Optional

import httpx


async def call_api(client: httpx.AsyncClient, url: str,
                   timestamp: Optional[str] = None) -> dict[str, Any]:
    """Call Wayback Machine API and return JSON response.

    If API is unresponsive, sleep task for five seconds for a maximum of five times.
    After five unsuccessful attempts, exit program.

    Expect the following API responses:

    - URL with correctly formatted timestamp (YYYYMMDDhhmmss):
        JSON with nearest snapshot, latest snapshot if timestamp was not found
    - URL without timestamp:
        JSON with latest snapshot available
    - Any URL with badly formatted timestamp (e.g. 'May2000'):
        Empty JSON
    - URL that is has not available in archive.org:
        Empty JSON

    Args:
        client (httpx.AsyncClient): HTTPX AsyncClient to make API calls
        url (str): URL to be searched in the Wayback Machine
        timestamp (Optional[str]): Timestamp for desired snapshot

    Returns:
        dict[str, Any]: JSON API response
    """
    # Construct URL for API call
    api_call: str = f"https://archive.org/wayback/available?url={url}"
    if timestamp:
        api_call += f"&timestamp={timestamp}"
    # Call API
    tries: int = 0
    while tries < 5:
        try:
            response: httpx.Response = await client.get(api_call)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            tries += 1
            print("Encountered HTTP error, waiting 5 seconds.")
            await asyncio.sleep(5)
            continue
    else:
        sys.exit("API unresponsive, try again later.")


def get_closest(api_response: dict[str, Any]) -> Optional[str]:
    """Get URL of closest snapshot from API response if available.

    Returns None if API response is empty.

    Args:
        api_response: dict[str, Any]: API response as JSON

    Returns:
        Optional[str]: URL of Wayback Machine snapshot, if any was found
    """
    if not api_response['archived_snapshots']:
        return None
    return api_response['archived_snapshots']['closest']['url']


async def gather_snapshots(
        urls: list[str], timestamp: str = None) -> dict[str, Optional[str]]:
    """Create HTTPX session for API calls and return gathered snapshots.

    To make asynchronous calls, create a task list for calling the call_api function
    and get results with asyncio.gather(). The completed tasks will then be used to
    build a dict of url-snapshot pairs.

    Args:
        urls (list[str]): Urls to send to the Wayback Machine API
        timestamp (Optional[str]): Timestamp to send to the Wayback Machine API

    Returns:
        dict[str, Optional[str]]: API call results with original URL as keys and Wayback
                                  snapshot URLs as values
    """
    async with httpx.AsyncClient(timeout=10) as client:
        # Create task list (with each task being an API call)
        tasks: list[asyncio.Task[Any]] = []
        for url in urls:
            tasks.append(asyncio.create_task(call_api(client, url, timestamp)))
        # Execute tasks and gather results
        api_responses: list[dict[str, Any]] = await asyncio.gather(*tasks)
        # Build url-snapshot pairs from results
        wayback_urls: dict[str, Optional[str]] = {}
        for api_response in api_responses:
            wayback_urls[api_response["url"]] = get_closest(api_response)
    return wayback_urls
