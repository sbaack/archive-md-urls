"""Variables for test files to be shared across test modules."""

from pathlib import Path

# First test file contains date in meta block and file name
TEST_MD1 = Path("tests/test_data/2014-04-28-fake-blogpost.md")
TEST_MD1_SOURCE: str = TEST_MD1.read_text(encoding='utf-8')
# Second test file doesn't contain any date
TEST_MD2 = Path("tests/test_data/fake-blogpost-no-filename-date.md")
TEST_MD2_SOURCE: str = TEST_MD2.read_text(encoding='utf-8')
# Third test file only contains date in file name
TEST_MD3 = Path("tests/test_data/2014-04-28-fake-blogpost-no-meta.md")
TEST_MD3_SOURCE: str = TEST_MD3.read_text(encoding='utf-8')
# Fourth, a file that uses YAML front matter
TEST_YAML = Path("tests/test_data/2014-04-28-fake-blogpost_yaml.md")
TEST_YAML_SOURCE = TEST_YAML.read_text(encoding='utf-8')
# Finally, a version of TEST_MD1 with updated URLs
CONVERTED_FILE = Path("tests/test_data/2014-04-28-fake-blogpost_converted_urls.md")
CONVERTED_SOURCE: str = CONVERTED_FILE.read_text(encoding='utf-8')
