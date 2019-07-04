import pytest

from pyregions import standard_definition
from pyregions.parsers import parse_table


@pytest.fixture
def columnmap() -> standard_definition.RequiredColumns:
	return standard_definition.RequiredColumns()


def test_convert_row_to_standard_series_using_default_column_names(columnmap):
	data = {
		'regionCode':        'PRI', 'seriesCode': 'LP', 'regionName': 'Puerto Rico', 'seriesName': 'Population',
		'seriesDescription': 'standardDescription',
		'seriesUnits':       'Persons', 'seriesScale': 'Millions', '1980': 3.2, '1981': 3.22,
		'1982':              3.26, '1983': 3.286, '1984': 3.3, '1985': 3.3
	}

	expected = standard_definition.StandardSeries(
		region_name = 'Puerto Rico',
		region_code = 'PRI',
		series_name = 'Population',
		series_code = 'LP',
		description = 'standardDescription',
		notes = "",
		tags = [],
		units = 'Persons',
		scale = 'mega',
		values = [(1980, 3.2), (1981, 3.22), (1982, 3.26), (1983, 3.286), (1984, 3.3), (1985, 3.3)]

	)
	result = parse_table._convert_table_row_to_standard_series(data, columnmap)
	assert expected == result


def test_convert_row_to_standard_series_using_custom_column_names(columnmap):
	columnmap.scale_column = 'scaleabc'
	columnmap.name_column = 'series'
	data = {
		'regionCode':        'PRI', 'seriesCode': 'LP', 'regionName': 'Puerto Rico', 'series': 'Population',
		'seriesDescription': 'standardDescription',
		'seriesUnits':       'Persons', 'scaleabc': 'Millions', '1980': 3.2, '1981': 3.22,
		'1982':              3.26, '1983': 3.286, '1984': 3.3, '1985': 3.3
	}

	expected = standard_definition.StandardSeries(
		region_name = 'Puerto Rico',
		region_code = 'PRI',
		series_name = 'Population',
		series_code = 'LP',
		description = 'standardDescription',
		notes = "",
		tags = [],
		units = 'Persons',
		scale = 'mega',
		values = [(1980, 3.2), (1981, 3.22), (1982, 3.26), (1983, 3.286), (1984, 3.3), (1985, 3.3)]

	)
	result = parse_table._convert_table_row_to_standard_series(data, columnmap)
	assert expected == result

