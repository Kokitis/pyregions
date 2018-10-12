from pathlib import Path
from pyregions.parsers import parse_table
from pyregions.standard_table_definition import StandardTable, RequiredColumns


def parse_weo(path: Path) -> StandardTable:
	columns = RequiredColumns(
		region_name_column = 'Country',
		region_code_column = 'ISO',
		series_code_column = 'WEO Subject Code',
		series_name_column = 'Subject Descriptor',
		series_note_column = 'Country/Series-specific Notes',
		series_scale_column = 'Scale',
		series_units_column = 'Units',
		series_description_column = 'Subject Notes',
		series_tag_column = None
	)

	return parse_table(path, columns)




if __name__ == "__main__":
	filename = Path.home() / "Documents" / "GitHub" / "pyregions" / "data" / "WEOApr2018all.xlsx"

	table = parse_weo(filename)
	print(table.to_string())
