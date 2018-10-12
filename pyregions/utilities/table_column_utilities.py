from typing import List, Union, Tuple, Iterable, Any
from itertools import filterfalse
from pyregions.standard_table_definition import RequiredColumns


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

def column_heuristic(columns, **kwargs):
	""" Classifies the key columns that *must* be present in order to import a spreadhseet.
		Parameters
		----------
		columns: list<str>
			The columns present in the table.

		Keyword Arguments
		-----------------

		Notes
		-----
			This method identifies which columns contain information
			related to the region and subject.
	"""
	detected_columns = get_required_columns(columns, **kwargs)
	region_code_column = detected_columns['regionCodeColumn']
	region_name_column = detected_columns['regionNameColumn']
	series_code_column = detected_columns['seriesCodeColumn']
	series_name_column = detected_columns['seriesNameColumn']

	series_note_column = detected_columns['seriesNoteColumn']
	series_tag_column = detected_columns['seriesTagColumn']
	series_unit_column = detected_columns['seriesUnitNameColumn']
	series_scale_column = detected_columns['seriesScaleColumn']
	series_description_column = detected_columns['seriesDescriptionColumn']

	# Check if any selection methods were included as kwargs
	_region_code_column_keyword = kwargs.get('regionCodeColumn')
	_region_name_column_keyword = kwargs.get('regionNameColumn')
	_series_code_column_keyword = kwargs.get('seriesCodeColumn', kwargs.get('subjectCodeColumn'))
	_series_name_column_keyword = kwargs.get('seriesNameColumn', kwargs.get('subjectNameColumn'))

	# Check if any of the column keywords is overridden by kwargs.

	if _region_code_column_keyword:
		region_code_column = _region_code_column_keyword

	if _region_name_column_keyword:
		region_name_column = _region_name_column_keyword

	if _series_code_column_keyword:
		series_code_column = _series_code_column_keyword

	if _series_name_column_keyword:
		series_name_column = _series_name_column_keyword

	series_note_map = kwargs.get('seriesNoteMap')
	series_tag_map = kwargs.get('seriesTagMap')
	series_description_map = kwargs.get('seriesDescriptionMap')
	series_scale_map = kwargs.get('seriesScaleMap')
	series_unit_map = kwargs.get('seriesUnitMap')

	if series_note_map:
		series_note_column = series_note_map

	if series_tag_map:
		series_tag_column = series_tag_map

	if series_description_map:
		series_description_column = series_description_map

	if series_scale_map:
		series_scale_column = series_scale_map
	if series_unit_map:
		series_unit_column = series_unit_map

	column_config = {
		'regionCodeColumn':        region_code_column,
		'regionNameColumn':        region_name_column,
		'seriesCodeColumn':        series_code_column,
		'seriesNameColumn':        series_name_column,

		'seriesNoteColumn':        series_note_column,
		'seriesTagColumn':         series_tag_column,
		'seriesDescriptionColumn': series_description_column,
		'seriesScaleColumn':       series_scale_column,
		'seriesUnitColumn':        series_unit_column,

		'seriesNoteMap':           series_note_map,
		'seriesTagMap':            series_tag_map,
		'seriesDescriptionMap':    series_description_map,
		'seriesScaleMap':          series_scale_map,
		'seriesUnitMap':           series_unit_map
	}

	return column_config
if __name__ == "__main__":
	pass
