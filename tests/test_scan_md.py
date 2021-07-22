import unittest
from typing import Any
from unittest import mock

from archive_md_urls import scan_md
from tests.testfiles import (TEST_MD1, TEST_MD1_SOURCE, TEST_MD2,
                             TEST_MD2_SOURCE, TEST_MD3, TEST_MD3_SOURCE,
                             TEST_YAML_SOURCE)


class TestScanMD(unittest.TestCase):
    """Test functions in scan_md."""

    def test_filter_urls(self) -> None:
        """Test if URL lists are correctly filtered."""
        html, date = scan_md.convert_markdown(TEST_MD1_SOURCE)
        urls: list[str] = scan_md.get_urls(html)
        # Filtered list should only contain example.com and both Github URLs
        correct_filtered_result: list[str] = [
            "example.com", "github.com", "https://github.com/pypa/pip"
        ]
        # Result from filter_urls should have correct length and should contain
        # all elements of filtered_result
        self.assertEqual(len(scan_md.filter_urls(urls)), 3)
        self.assertTrue(
            all(url in scan_md.filter_urls(urls) for url in correct_filtered_result)
        )
        # Filtering STABLE_URLS should result in empty list
        self.assertEqual(scan_md.filter_urls(scan_md.STABLE_URLS), [])

    def test_format_date(self) -> None:
        """Test if date is correctly formatted or returned as None."""
        # Accepted inputs and expected results
        self.assertEqual(scan_md.format_date("2010-03-07"), "201003070000")
        self.assertEqual(scan_md.format_date("2013-04-11 14:50"), "201304111450")
        self.assertEqual(scan_md.format_date("2015-05-17 17:49:59"), "201505171749")
        self.assertEqual(scan_md.format_date("20.08.2018"), "201808200000")
        # Hugo default
        self.assertEqual(
            scan_md.format_date("2019-03-26T08:47:11+01:00"), "201903260847"
        )
        # A human readable date string
        self.assertEqual(
            scan_md.format_date("Monday, October 10, 2014"), "201410100000"
        )
        # Various inputs that should raise dateutil ParserError and thus return None
        self.assertEqual(scan_md.format_date("some wrong string"), None)
        self.assertEqual(scan_md.format_date("2014-04-10 13:10:99"), None)

    def test_convert_markdown(self) -> None:
        """Test if date correctly extracted from metadata."""
        html, date = scan_md.convert_markdown(TEST_MD1_SOURCE)
        self.assertEqual(date, "2014-04-28")
        html, date = scan_md.convert_markdown(TEST_YAML_SOURCE)
        self.assertEqual(date, "2014-04-28")
        html, date = scan_md.convert_markdown(TEST_MD2_SOURCE)
        self.assertEqual(date, None)
        html, date = scan_md.convert_markdown(TEST_MD3_SOURCE)
        self.assertEqual(date, None)

    def test_get_urls(self) -> None:
        """Test if URLs are correctly extracted from HTML."""
        html, date = scan_md.convert_markdown(TEST_MD1_SOURCE)
        # All URLs contained in the test file
        full_url_list: list[str] = [
            "example.com", "example.com",
            "github.com", "https://github.com/pypa/pip",
            "https://web.archive.org/web/20000622042643/http://www.google.com/",
            "https://doi.org/10.1080/32498327493.2014.358732798",
            "{filename}/blog/2012/2012-02-05-an-even-older-blogpost.md"
        ]
        self.assertEqual(scan_md.get_urls(html), full_url_list)

    @mock.patch("archive_md_urls.scan_md.format_date")
    def test_scan_md(self, mock_format_date: Any) -> None:
        """Test if format_date is called with correct value."""
        # No date at all should result in calling format_date with trimmed string
        scan_md.scan_md(TEST_MD2_SOURCE, TEST_MD2)
        mock_format_date.assert_called_with("fake-blogp")
        # Test with date in metadata
        scan_md.scan_md(TEST_MD1_SOURCE, TEST_MD1)
        mock_format_date.assert_called_with("2014-04-28")
        # Test with date in file name only
        scan_md.scan_md(TEST_MD3_SOURCE, TEST_MD3)
        mock_format_date.assert_called_with("2014-04-28")
