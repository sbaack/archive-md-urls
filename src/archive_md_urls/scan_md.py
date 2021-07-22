"""Extract dates and URLs from Markdown files."""

from pathlib import Path
from typing import Optional

import dateutil.parser
import markdown
from bs4 import BeautifulSoup

# List of URLs considered stable and thus ignored
STABLE_URLS: tuple[str, ...] = (
    # archive.org snapshots
    "web.archive.org/web/",
    # Pelican intra-site links
    "{filename}",
    "{static}",
    # Jekyll intra-site links
    "{% post_url",
    # Hugo intra-site links
    "{{< ref",
    "{{< relref",
    # Persistent identifier list from ORCID (https://pub.orcid.org/v2.0/identifiers)
    "https://arxiv.org/abs/",
    "http://www.amazon.com/dp/",
    "https://www.authenticus.pt/",
    "http://adsabs.harvard.edu/abs/",
    "https://ciencia.iscte-iul.pt/id/",
    "https://d-nb.info/",
    "https://doi.org/",
    "http://ethos.bl.uk/OrderDetails.do?uin=",
    "https://hal.archives-ouvertes.fr/view/resolver/",
    "http://hdl.handle.net/",
    "https://www.worldcat.org/isbn/",
    "https://portal.issn.org/resource/ISSN/",
    "http://zbmath.org/?format=complete&q=an%3A",
    "http://www.jstor.org/stable/",
    "https://koreamed.org/article/",
    "http://lccn.loc.gov/",
    "https://www.lens.org/",
    "http://www.ams.org/mathscinet-getitem?mr=",
    "http://www.worldcat.org/oclc/",
    "http://openlibrary.org/b/",
    "https://www.osti.gov/biblio/",
    "http://identifiers.org/pdb/",
    "https://europepmc.org/articles/",
    "https://www.ncbi.nlm.nih.gov/pubmed/",
    "https://europepmc.org/article/PPR/",
    "https://tools.ietf.org/html/",
    "https://identifiers.org/rrid/",
    "http://papers.ssrn.com/abstract_id=",
    "http://zbmath.org/?format=complete&q="
)


def scan_md(md_source: str, md_file: Path) -> tuple[Optional[str], list[str]]:
    """Extract date and URLs from specified Markdown file.

    To get the date, first try to extract it from Markdown meta information. If no date
    found, try to extract date from file name by following the Jekyll naming convention
    where files for blog posts start with YYYY-MM-DD. Next, try to format date for
    Wayback Machine API as YYYYMMDDhhmm.

    Args:
        md_source (str): Contents of the Markdown file
        md_file (Path): Markdown file path

    Returns:
        tuple[Optional[str], list[str]]: Formatted date (if found) and list of URLs
    """
    html, date = convert_markdown(md_source)
    if not date:
        date = md_file.name[:10]
    return format_date(date), filter_urls(get_urls(html))


def convert_markdown(md_source: str) -> tuple[str, Optional[str]]:
    """Convert Markdown file to HTML and extract date from metadata.

    Args:
        md_file (str): Contents of the Markdown file

    Returns:
        tuple[str, dict[str, Optional[str]]: HTML version of Markdown file and date from
                                             Markdown metadata
    """
    md: markdown.core.Markdown = markdown.Markdown(extensions=['meta'])
    html: str = md.convert(md_source)
    try:
        date: Optional[str] = md.Meta['date'][0]
    except KeyError:
        date = None
    return html, date


def format_date(date: str) -> Optional[str]:
    """Format date according to Wayback Machine API format.

    Use dateutil.parser to recognize dates and return them as YYYYMMDDhhmm. If hour and
    minute aren't provided, they are set to 0. If format isn't recognized, return None.

    Args:
        date (str): Date extracted from Markdown metadata or file name

    Returns:
        Optional[str]: Date formatted as YYYYMMDDhhmm
    """
    try:
        return dateutil.parser.parse(date).strftime("%Y%m%d%H%M")
    # Malformatted date or no date at the beginning of file name
    except dateutil.parser._parser.ParserError:
        return None


def filter_urls(md_urls: list[str]) -> list[str]:
    """Take and filter list of URLs for API calls.

    Filter out duplicates and remove URLs that are considered stable:

    - URLs that already point to archive.org
    - Intra-site links (recognizes Pelican, Jekyll and Hugo intra-site link formats)
    - URLs containing stable identifiers

    Args:
        md_urls (list[str]): List of URLs extracted from Markdown file

    Returns:
        list[str]: Filtered list of URLs
    """
    # Remove duplicates
    urls: list[str] = list(set(md_urls))
    # Filter out stable URLs
    return [url for url in urls if not
            any(stable_url in url for stable_url in STABLE_URLS)]


def get_urls(html: str) -> list[str]:
    """Extract links from converted Markdown HTML.

    Args:
        html (str): HTML version of Markdown file

    Returns:
        list[str]: URLs found in HTML
    """
    soup = BeautifulSoup(html, "html.parser")
    return [a.get('href') for a in soup.find_all('a', href=True)]
