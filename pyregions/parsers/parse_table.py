from pathlib import Path
from pyregions import StandardTable, StandardSeries, RequiredColumns
from pyregions.utilities import get_table
from pytools.numbertools import to_number



def load_standard_table(path: Path, column_map: RequiredColumns = RequiredColumns()) -> StandardTable:
	""" Imports a table formatted with annual data in each column."""
	table, numeric_columns = get_table(path)
	column_map.find_missing_columns(table.columns)
	parsed_table = StandardTable()

	for index, row in table.iterrows():

		region_name = row[column_map.region_name_column]
		region_code = row[column_map.region_code_column]

		series_name = row[column_map.series_name_column]
		series_code = row[column_map.series_code_column]
		series_description = row[column_map.series_description_column]
		series_notes = row.get(column_map.series_note_column)
		series_units = row[column_map.series_units_column]
		series_scale = row[column_map.series_scale_column]
		series_tags = row.get(column_map.series_tag_column, [])

		series_values = [(col, row[col]) for col in numeric_columns]
		series_values = [(int(i), to_number(j)) for i, j in series_values]

		series = StandardSeries(
			region_name = region_name,
			region_code = region_code,
			series_name = series_name,
			series_code = series_code,
			series_description = series_description,
			series_notes = series_notes,
			series_units = series_units,
			series_scale = series_scale,
			series_tags = series_tags,

			series_values = series_values
		)
		parsed_table.data.append(series)

	return parsed_table

if __name__ == "__main__":

	filename = Path.cwd() / "tests" / "standard_table.tsv"

	t = load_standard_table(filename)
	print(t.to_yaml())


