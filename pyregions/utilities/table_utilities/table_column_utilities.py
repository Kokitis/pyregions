from typing import List, Union, Tuple, Iterable, Any
from itertools import filterfalse
from dataclasses import dataclass


@dataclass  # For clarity
class RequiredColumns:
	region_code_column: str
	region_name_column: str
	series_code_column: str
	series_name_column: str
	series_note_column: str
	series_scale_column: str
	series_unitname_column: str
	series_unitcode_column: str
	series_description_column: str
	series_tag_column: str


def parse_keywords(columns: Iterable[Any], candidates: List[str]):
	"""	Matches values in `columns` that are present in `candidates`
		Parameters
		----------
			columns: Iterable[str]
				A list of the columns in the table.
			candidates: List[str]
				A list of the possible column names that hold the
				desired information.
				Ex. `country`, `regionName`, `countryName` to
				extract the column with the region's name
	"""

	candidates = [col for col in columns if col in candidates]
	if len(candidates) == 0:
		value = None
	else:
		value = candidates[0]

	return value


def is_number(value: Union[int, float, str]) -> bool:
	""" Checks if a value is a numeric type or if all characters in the string are digits.
		Parameters
		----------
			value: int, float, str
	"""
	is_numeric_type = isinstance(value, (int, float))
	is_all_digit = is_numeric_type or (isinstance(value, str) and value.isdigit())
	return is_all_digit


def separate_table_columns(columns: List[Any]) -> Tuple[List[Any], List[Any]]:
	""" Separates a list of columns into 'years' and 'other'. The `years` list conserves the column type
		as represented in the original table.
		Parameters
		----------
			columns: list<str,int>
				The column list. Year columns may be represented
				by either number or strings of numeric digits.
		Returns
		-------
			years, other_columns: Tuple[List[Any], List[Any]]
	"""
	years = filter(is_number, columns)
	other_columns = filterfalse(is_number, columns)
	return list(years), list(other_columns)


def _getColumnName(columns, keys):
	if len(keys) == 0:
		return None
	elif len(keys) == 1:
		return keys[0] if keys[0] in columns else None
	elif keys[0] in columns:
		return keys[0]
	else:
		return _getColumnName(columns, keys[1:])


def get_required_columns(table_columns: Iterable[Any], **kwargs)->RequiredColumns:
	""" Attempts to retrieve the required columns that are needed
		to import a table into the database. 
		Parameters
		----------
			table_columns: Iterable[Any]
		Keyword Arguments
		-----------------
		- `regionCodeColumn`
		- `regionNameColumn`
		- `seriesCodeColumn`
		- `seriesNameColumn`
		- `seriesNoteColumn`
		- `unitNameColumn`
		- `unitCodeColumn`
		- `scaleColumn`
		- `seriesDescriptionColumn`

	"""
	region_code_column = parse_keywords(table_columns, [
		'regionCode', 'countryCode', 'isoCode', 'fipsCode', 'stateCode', kwargs.get('regionCodeColumn')
	])

	region_name_column = parse_keywords(table_columns, [
		'regionName', 'countryName', 'state', 'countyName', 'cityName', kwargs.get('regionNameColumn')
	])

	series_code_column = parse_keywords(table_columns, [
		'seriesCode', 'subjectCode', 'variable', 'subjectCodeColumn', 'subjectCodeColumn', 'seriesCodeColumn',
		kwargs.get('seriesCodeColumn')
	])

	series_name_column = parse_keywords(table_columns, [
		'seriesName', 'subjectName', 'subjectNameColumn', 'seriesNameColumn', kwargs.get('seriesNameColumn')
	])

	series_note_column = parse_keywords(table_columns, [
		'notes', 'subjectNotes', 'seriesNotes', kwargs.get('seriesNoteColumn')
	])

	series_scale_column = parse_keywords(table_columns, [
		'scale', 'multiplier', 'seriesScale', kwargs.get('scaleColumn')
	])

	series_unit_name_column = parse_keywords(table_columns, [
		'units', 'unit', 'Unit', 'Units', 'seriesUnit',
		'seriesUnits', 'subjectUnits', 'subjectUnit', kwargs.get('unitNameColumn')
	])

	series_unit_code_column = parse_keywords(table_columns, [
		'unitCode', 'seriesUnitCode', kwargs.get('unitCodeColumn')
	])

	series_description_column = parse_keywords(table_columns, [
		'seriesDescription', 'subjectDescription', 'description', kwargs.get('seriesDescriptionColumn')
	])

	series_tag_column = parse_keywords(table_columns, [
		'seriesTags', 'subjectTags', 'tags'
	])

	result = RequiredColumns(
		region_code_column,
		region_name_column,
		series_code_column,
		series_name_column,
		series_note_column,
		series_scale_column,
		series_unit_name_column,
		series_unit_code_column,
		series_description_column,
		series_tag_column
	)
	return result


if __name__ == "__main__":
	pass
