from pathlib import Path
from pyregions.utilities.table_utilities import _get_delimiter, get_numeric_columns, get_table, load_table

import pytest
class TestClass:
	# To test whether the class of an object matters.
	pass

@pytest.mark.parametrize(
	"string,expected",
	[
		("abc.tsv", "\t"),
		("abc.csv", ",")
	]
)
def test_get_delimiter(string, expected):
	result = _get_delimiter(string)
	assert result == expected

@pytest.mark.parametrize(
	"columns,expected",
	[
		(['wgwE', 123, 'afhr', ' 1,245.34 ', '123'], [123, ' 1,245.34 ', '123']),
		(['abcdef', 123, 456, TestClass, TestClass(), 789], [123, 456, 789])
	]
)
def test_get_numeric_columns(columns, expected):
	result = get_numeric_columns(columns)
	assert expected == result