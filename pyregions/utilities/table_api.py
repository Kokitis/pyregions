import progressbar
"""
from pyregions.widgets import tables
from pyregions.github import tabletools, pprint, timetools, numbertools
from math import isnan
from pyregions.widgets.validation import ValidateApiResponse
from typing import List, Dict, union
"""

from typing import List, Dict, Union, Tuple, Mapping
from pyregions.utilities import load_table, save_table
from pyregions.utilities.table_utilities import get_required_columns
from pathlib import Path
from dataclasses import dataclass, asdict
PathType = Union[str, Path]
Row = Mapping
SeriesValues = List[Tuple[Union[str, timetools.Timestamp], float]]

import pandas




class TableApi:
	""" Designed to parse a spreadsheet and import it into the database.
		Parameters
		----------
		filename: str, Table
		report: dict
			Details concerning the report.
			* 'name': str
				The name of the report
			* 'publishDate': str
				The date the report was published
			* 'retrieveDate': str
				The date the report was looked up.
			* 'url': str
				A website url that contains the dataset or has further information on the dataset.
		agency: dict<>
			*'name': str

		Keyword Arguments
		-----------------
		- `tableConfig`: dict
			Arguments to pass to pandas.DataFrame()
		- `startDay`: str; default '01-01'

		- `blacklist`: list<str>
			A list of series names or codes to skip when processing the table.
		- `whitelist`: list<str>
			If provided, only the listed series will be imported. Overrides 'blacklist'.

		- `seriesCodeColumn`: str
		- `seriesNameColumn`: str
		- `regionCodeColumn`: str, dict<str,str>
		- `regionNameColumn`: str

		- `seriesTagColumn`: str
			Either the column containing tags for the series for the series, or a dictionary
			mapping series codes to relevant tags.
		- `seriesNoteColumn` str
			Dictionary keys should be strings of the form 'region_code|subject_code'. region_code defaults to None.
		- `seriesDescriptionColumn`: str


		- `yearRange`: tuple(int, int)
			Filters out any values that occur in years outside the supplied range.
			Ex. (1900, None) -> Filters out years below 1900, but has no upper bound.
			Ex. (1900, 2000) -> Only years with ine range [1900, 2000] will be included.
		Returns
		-------
		Dict
	"""

	def __init__(self, filename: PathType, **kwargs):
		kwargs['startDay'] = kwargs.get('startDay', '01-01')

		file_kwargs = kwargs.get('tableConfig', dict())
		namespace_key: str = kwargs.get('namespace')
		report: Dict[str, str] = kwargs.get('report')
		agency: Dict[str, str] = kwargs.get('agency')

		report_table = load_table(filename)

		table_column_map = get_required_columns(report_table.columns, **kwargs)

		region_list: List[str] = self._parseTable(report_table, **kwargs)

		report_information = {
			'report':    report,
			'agency':    agency,
			'namespace': namespace_key,
			'regions':   region_list
		}

		self.data = report_information




	def _parseTable(self, table, **kwargs):
		""" Imports a spreadsheet into the database.
			Parameters
			----------
			filename: str, tabletools.Table, pandas.DataFrame
				The file path of the table to import. Should be compatible with tabletools.Table.

		"""

		# Get the relevant columns for the data.

		report_columns = self._getColumnNames(table.columns, **kwargs)
		# pprint(report_columns)
		api_table = list()
		print("Converting the table into a compatible json format...")

		region_groups = table.groupby(by = report_columns['regionCodeColumn'])
		index = 0
		pbar = progressbar.ProgressBar(max_value = len(region_groups))
		for region_code, region_group in region_groups:
			index += 1
			pbar.update(index)

			report_region = self._parseRegion(region_code, region_group, report_columns, **kwargs)
			api_table.append(report_region)

		return api_table

	def _parseRegion(self, region_code, region_group, columns, **kwargs):
		"""
			Parses all rows belonging to a single region from a table.
		Parameters
		----------
		region_code: str
		region_group: pandas.DataFrame
		columns: dict<>
		kwargs

		Returns
		-------
		dict<>
			* 'regionName': str
			* 'regionCode': str
			* 'regionSeries': list<dict<>>
		"""
		region_series = list()
		region_name = region_group[columns['regionNameColumn']].values[0]
		for index, row in region_group.iterrows():

			current_series = self._convertRow(row, columns, **kwargs)

			if current_series and len(current_series['seriesValues']) != 0:
				region_series.append(current_series)

		region_information = {
			'regionName':   region_name,
			'regionCode':   region_code,
			'regionType':   'country',
			'regionSeries': region_series
		}

		return region_information

	def _convertRow(self, row: Row, report_columns: Dict, **kwargs):
		""" Converts a row into an importable dict.
			Parameters
			----------
			row: dict, pandas.Series
			report_columns: dict

			Keyword Arguments
			-----------------
				* unitMap: dict<tuple,dict>
				* scaleMap: dict<tuple,dict>
				* tagMap: dict<tuple,dict>
				* 'yearRange': tuple<>
				* 'regionCodeMap': dict<str,str>
					Overrides regionCodeColumn
				* descriptionMap: dict<tuple, dict>
				* blacklist: list<>
					A list of series keys to skip when importing a table.
				* whitelist: list<>
					Overrides the blacklist. Only the series key contained in
					the whitelist will be imported.
		"""
		# Confirm that all required components exist.
		blacklist: List[str] = kwargs.get('blacklist', [])
		whitelist: List[str] = kwargs.get('whitelist', [])
		year_range = kwargs.get('yearRange', (None, None))

		region_code_column = kwargs['regionCodeColumn']
		region_code_map = kwargs.get('regionCodeMap') # overridds region_code_column



		# Should be static
		try:
			region_name: str = row[report_columns['regionNameColumn']]
			if region_code_map:
				region_code:str = region_code_map[region_name]
			else:
				region_code: str = row[report_columns['regionCodeColumn']]  # identifier


			subject_code: str = row[report_columns['seriesCodeColumn']]
			subject_name: str = row[report_columns['seriesNameColumn']]
		except KeyError as exception:
			error_message = {
				'exception':        exception,
				'exceptionMessage': str(exception),
				'parameters':       {
					'row':            row,
					'report_columns': report_columns,
					'kwargs':         kwargs
				}
			}
			pprint(error_message)
			raise exception

		_in_whitelist: bool = len(whitelist) != 0 or subject_code in whitelist
		_not_in_blacklist: bool = len(whitelist) == 0 and subject_code not in blacklist
		use_row: bool = _in_whitelist or _not_in_blacklist

		if use_row:

			series_code_column: str = report_columns.get('seriesCodeColumn')
			series_code: str = row[series_code_column]
			SeriesMap = Union[str, Dict[str, str]]
			series_unit_map: SeriesMap = report_columns.get('seriesUnitColumn')
			if not series_unit_map:
				series_unit_map = report_columns.get('seriesUnitMap')

			series_scale_map: SeriesMap = report_columns.get('seriesScaleColumn')
			if not series_scale_map:
				series_scale_map = report_columns.get('seriesScaleMap')

			series_tag_map: SeriesMap = report_columns.get('seriesTagColumn')
			if not series_tag_map:
				series_tag_map = report_columns.get('seriesTagMap')

			series_note_map: SeriesMap = report_columns.get('seriesNoteColumn')
			if not series_note_map:
				series_note_map = report_columns.get('seriesNoteMap')

			series_description_map: SeriesMap = report_columns.get('seriesDescriptionColumn')
			if not series_description_map:
				series_description_map = report_columns.get('seriesDescriptionMap')

			series_units = self._getMetadata(row, series_unit_map, series_code)
			series_scale = self._getMetadata(row, series_scale_map, series_code)
			series_tags = self._getMetadata(row, series_tag_map, series_code)
			series_notes = self._getMetadata(row, series_note_map, series_code, region_code)
			series_description = self._getMetadata(row, series_description_map, series_code)

			if series_tags is None:
				series_tags = []
			elif isinstance(series_tags, str):
				series_tags = series_tags.split('|')
			if series_scale is None:
				series_scale = 'unit'
			if series_notes is None:
				series_notes = ''

			series_values: SeriesValues = self._getValues(row, kwargs['startDay'], kwargs['jsonCompatible'], year_range)

			json_series = {
				'regionCode':        region_code,
				'regionName':        region_name,
				'seriesName':        subject_name,
				'seriesCode':        subject_code,
				'seriesScale':       series_scale,

				'seriesNotes':       series_notes,
				'seriesDescription': series_description,
				'seriesTags':        series_tags,
				'seriesUnits':       series_units,
				'seriesValues':      series_values
			}
		else:
			json_series = None

		return json_series

	@staticmethod
	def _getValues(row: Row, start_day: str, json_compatible: bool, year_range:Tuple) -> SeriesValues:
		""" Dates may take to following formats:
			* int, float: ex. 2017, 2017.0
			* str ex. '2017', '2017-03-21'
			* datetime object
		"""
		min_year, max_year = year_range
		year_columns, _ = tables.separateTableColumns(row.keys())

		# Check if the years include date information.
		fy = year_columns[0]

		if isinstance(fy, (int, float)) or (isinstance(fy, str) and fy.isdigit()):
			values = [(str(int(y)) + '-' + start_day, row[y]) for y in year_columns]
		else:
			values = [(y, row[y]) for y in year_columns]

		values = [(i, numbertools.toNumber(j)) for i, j in values]
		values = [(timetools.Timestamp(i), j) for i, j in values if not isnan(j)]

		if min_year:
			values = [i for i in values if i[0].toYear() >= min_year]
		if max_year:
			values = [i for i in values if i[0].toYear() <= max_year]

		if json_compatible:
			values = [(i.toIso(), j) for i, j in values]
		return values

	@staticmethod
	def _getMetadata(row: Row, metadata_map, subject_code, region_code = None):
		"""
			Extracts metadata from the row.
		Parameters
		----------
		row: pandas.Series
			The row to extract metadata from.
		metadata_map: str, dict<>
			The label of the column containing the desired metadata or a dictionary mapping the
			series code to metadata values.
		subject_code: str
		region_code: str; default None

		Returns
		-------
			str
		"""

		if isinstance(metadata_map, str) and metadata_map in row.keys():
			metadata_value = row[metadata_map]
		elif isinstance(metadata_map, dict):
			if region_code:
				metadata_key = region_code + '|' + subject_code
			else:
				metadata_key = subject_code
			metadata_value = metadata_map.get(metadata_key)
		else:
			error_message = {
				'parameters': {
					'metadata_map':   metadata_map,
					'subject_column': subject_code,
					'row':            row.keys()
				}
			}
			pprint(error_message)
			raise ValueError
		if isinstance(metadata_value, float) and isnan(metadata_value):
			metadata_value = None
		return metadata_value
