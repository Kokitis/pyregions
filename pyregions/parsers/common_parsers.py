from pathlib import Path

from pyregions.parsers import read_standard_table
import pyregions.standard_definition as sd
from infotools import timetools

def read_weo(path: Path, date:str) -> sd.StandardData:
	"""
		Reads a weo table and pre-fills most of the report information.
	Parameters
	----------
	path
	date: str
		The year and month in 'yyyy-dd' format.
	"""
	columns = sd.RequiredColumns(
		region_name_column = 'Country',
		region_code_column = 'ISO',
		code_column = 'WEO Subject Code',
		name_column = 'Subject Descriptor',
		note_column = 'Country/Series-specific Notes',
		scale_column = 'Scale',
		units_column = 'Units',
		description_column = 'Subject Notes',
		tag_column = None
	)

	year, month = date.split('-')
	# datasets are saved according to how many previous issues have been published the same year.
	month = '01' if int(month) < 5 else '02'
	date = timetools.Timestamp(date+'-01')
	report = sd.StandardReport(
		name = 'World Economic Outlook',
		agency = 'International Monetary Fund',
		url = f'https://www.imf.org/external/pubs/ft/weo/{year}/{month:>02d}/weodata/download.aspx',
		date = date
	)

	return read_standard_table(path, columns)


if __name__ == "__main__":
	filename = Path.home() / "Documents" / "GitHub" / "pyregions" / "data" / "WEOApr2018all.xlsx"

	table = parse_weo(filename)
	print(table.to_string())
