import unittest

from archive_md_urls import update_files
from tests.testfiles import CONVERTED_SOURCE, TEST_MD1_SOURCE

# Create correct URL-Snapshot pairs for TEST_MD1 file
WAYBACK_URLS: dict[str, str] = {
    "example.com":
        "http://web.archive.org/web/20140428170257/http://www.example.com/",
    "github.com":
        "http://web.archive.org/web/20140430012615/https://github.com",
    "https://github.com/pypa/pip":
        "http://web.archive.org/web/20130829090428/https://github.com/pypa/pip"
}


class TestUpdateFiles(unittest.TestCase):
    """Test if files are updated correctly."""

    def test_update_source(self) -> None:
        """Test of Markdown source is correctly updated."""
        self.assertEqual(
            update_files.update_md_source(TEST_MD1_SOURCE, WAYBACK_URLS),
            # The CONVERTED_SOURCE file is identical to TEST_MD1_SOURCE but with
            # correctly updated URLs
            CONVERTED_SOURCE
        )
