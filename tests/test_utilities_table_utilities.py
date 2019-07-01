from pyregions.utilities import table_utilities
import pytest

@pytest.mark.parametrize(
	"columns,expected",
	[
		(['abc', '123', 456], ['123',456]),
		(["13.4", 'aslkjnsf12312ll'], ['13.4'])
	]
)
def test_get_numeric_columns(columns, expected):
	result = table_utilities.get_numeric_columns(columns)
	assert result == expected

@pytest.mark.parametrize(
	"value,expected",
	[
		("abc.tsv", '\t'),
		("assssdawrfa.csv", ','),
		("a.tab", "\t")
	]
)
def test_get_delimiter(value, expected):
	assert table_utilities._get_delimiter(value) == expected