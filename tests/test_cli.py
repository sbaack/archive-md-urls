import unittest
from pathlib import Path

from archive_md_urls import cli
from tests.testfiles import (CONVERTED_FILE, TEST_MD1, TEST_MD2, TEST_MD3,
                             TEST_YAML)


class TestCli(unittest.TestCase):
    """Test Markdown file searching."""

    def test_get_md_files(self) -> None:
        """Test if Markdown files are collected correctly."""
        # Create list of all files for recursive and non-recursive search in test_data
        all_files_recursive: list[Path] = [
            CONVERTED_FILE, TEST_MD1, TEST_MD2, TEST_MD3, TEST_YAML,
            Path("tests/test_data/subdir/empty_testfile.md")
        ]
        all_files_no_rec: list[Path] = [
            CONVERTED_FILE, TEST_MD1, TEST_MD2, TEST_MD3, TEST_YAML
        ]
        # Test single file
        self.assertEqual(cli.get_md_files([TEST_MD1], False), [TEST_MD1])
        # Test two individual files
        self.assertEqual(
            cli.get_md_files([TEST_MD1, TEST_MD2], False), [TEST_MD1, TEST_MD2]
        )
        # Test recursive search in test_data: First, check if all files are
        # included, then check if number of files is correct
        scanned_files_rec: list[Path] = cli.get_md_files(
            [Path("tests/test_data/")], True
        )
        self.assertTrue(
            all(file in scanned_files_rec for file in all_files_recursive)
        )
        self.assertEqual(
            len(scanned_files_rec), len(all_files_recursive)
        )
        # Same tests for non-recursive search in test_data
        scanned_files_no_rec: list[Path] = cli.get_md_files(
            [Path("tests/test_data/")], False
        )
        self.assertTrue(
            all(file in scanned_files_no_rec for file in all_files_no_rec)
        )
        self.assertEqual(
            len(scanned_files_no_rec), len(all_files_no_rec)
        )
        # Test combination of directories and single files that is effectively equal to
        # a recursive search in test_data
        scanned_files: list[Path] = cli.get_md_files(
            [Path("tests/test_data/"),
             Path("tests/test_data/subdir/empty_testfile.md")],
            False
        )
        self.assertEqual(scanned_files_rec, scanned_files)
