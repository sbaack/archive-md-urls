import unittest
from typing import Any

from archive_md_urls import gather_snapshots


class TestClosestSnapshot(unittest.TestCase):
    """Test functions for gathering snapshots."""

    def test_build_api_calls(self) -> None:
        """Test if correct URL is constructed for API calls."""
        # Base URL contained in every API call
        api_base: str = "https://archive.org/wayback/available?url="
        # Test with existing URL, first without and then with timestamp
        existing_url: str = "google.com"
        timestamp: str = "20140703"
        self.assertEqual(
            gather_snapshots.build_api_call(existing_url),
            f"{api_base}{existing_url}"
        )
        self.assertEqual(
            gather_snapshots.build_api_call(existing_url, timestamp),
            f"{api_base}{existing_url}&timestamp={timestamp}"
        )
        # Same tests again, but with invalid URL and bad timestamp
        non_existend_url: str = "www.dsjfhldsjf.com"
        bad_timestamp: str = "djshfjdls"
        self.assertEqual(
            gather_snapshots.build_api_call(non_existend_url),
            f"{api_base}{non_existend_url}"
        )
        self.assertEqual(
            gather_snapshots.build_api_call(non_existend_url, bad_timestamp),
            f"{api_base}{non_existend_url}&timestamp={bad_timestamp}"
        )

    def test_get_closest(self) -> None:
        """Test if correct value is returned given various API responses."""
        test_url: str = "http://web.archive.org/web/20210605231254/https://example.com/"
        # We ignore the 'available' status
        not_available: dict[str, Any] = {"archived_snapshots": {"closest":
                                                                {"available": False,
                                                                 "url": test_url}}}
        self.assertEqual(
            gather_snapshots.get_closest(not_available), test_url
        )
        # Empty API response =  None
        empty: dict[str, Any] = {"archived_snapshots": {}}
        self.assertEqual(
            gather_snapshots.get_closest(empty), None
        )
        # More generic regex test
        available: dict[str, Any] = {"archived_snapshots": {"closest":
                                                            {"available": True,
                                                             "url": test_url}}}
        self.assertRegex(
            gather_snapshots.get_closest(available),
            r"http://web.archive.org/web/\d+/https://example.com/"
        )
