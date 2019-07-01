from pathlib import Path
from typing import List, Mapping

import pandas
from infotools import numbertools

from pyregions import standard_definition as sd
from pyregions.utilities import get_table
from pyregions.utilities.table_utilities import get_numeric_columns


def _convert_table_row_to_standard_series(row: Mapping[str, str], column_map: sd.RequiredColumns) -> sd.StandardSeries:
	"""
	Parses a row from a table and returns a standardized series.
	Parameters
	----------
	row: pandas.Series
	column_map:RequiredColumns

	Returns
	-------
	StandardSeries

	Examples
	--------

	"""
	numeric_columns = get_numeric_columns(row.keys())
	region_name = row[column_map.region_name_column]
	region_code = row[column_map.region_code_column]

	series_name = row[column_map.name_column]
	series_code = row[column_map.code_column]
	series_description = row[column_map.description_column]

	series_units = row[column_map.units_column]
	series_scale = numbertools.get_scale(row[column_map.scale_column]).prefix
	series_notes = row.get(column_map.note_column, "")
	series_tags = row.get(column_map.tag_column, [])

	series_values = [(col, row[col]) for col in numeric_columns]
	series_values = [(int(i), numbertools.to_number(j)) for i, j in series_values]

	series = sd.StandardSeries(
		region_name = region_name,
		region_code = region_code,
		series_name = series_name,
		series_code = series_code,
		description = series_description,
		notes = series_notes,
		units = series_units,
		scale = series_scale,
		tags = series_tags,
		values = series_values
	)
	return series


def read_standard_table(path: Path, column_map: sd.RequiredColumns = sd.RequiredColumns()) -> List[sd.StandardSeries]:
	""" Imports a table formatted with annual data in each column."""
	table, numeric_columns = get_table(path)

	column_map.find_missing_columns(table.columns)

	parsed_series = [_convert_table_row_to_standard_series(row, column_map) for _, row in table.iterrows()]

	return parsed_series

def read_standard_data(path:Path, report:Mapping[str,str])->sd.StandardData:
	pass

if __name__ == "__main__":
	pass
