from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Tuple, Union

from infotools.timetools import Timestamp


@dataclass
class RequiredColumns:
	region_code_column: str = 'regionCode'
	region_name_column: str = 'regionName'
	code_column: str = 'seriesCode'
	name_column: str = 'seriesName'
	note_column: str = 'seriesNotes'
	scale_column: str = 'seriesScale'
	units_column: str = 'seriesUnits'
	description_column: str = 'seriesDescription'
	tag_column: Optional[str] = 'seriesTags'

	def find_missing_columns(self, columns: List[str]) -> List[str]:
		"""
			Determines which columns are missing from the table and need to be added.
		Parameters
		----------
		columns: A list of column labels to parse

		Returns
		-------
		Optional[List[str]]
			A list of the columns that need to be added to the table.
		"""
		missing_columns = list()

		# Compare the defined column names against those seen in the table.
		for name, value in asdict(self).items():
			if value not in columns and name not in ['tag_column', "note_column"]:
				missing_columns.append(value)

		# Check if some of the columns are mising.
		if len(missing_columns) > 0:
			message = f"The following columns are missing: {missing_columns}"
			raise ValueError(message)
		return missing_columns


@dataclass
class StandardRegion:
	code: str
	name: str
	type: str


@dataclass
class StandardReport:
	date: Timestamp
	name: str
	url: str
	agency: str


@dataclass
class StandardSeries:
	region_name: str
	region_code: str
	series_name: str
	series_code: str
	scale: str
	description: str
	notes: str
	units: str
	tags: List[str]
	values: List[Tuple[int, float]]

	def to_dict(self) -> Dict[str, Union[str, List]]:
		return asdict(self)

	def to_row(self) -> Dict[Union[int, str], Union[str, float]]:
		d = self.to_dict()

		d.update(d.pop('series_values'))
		return d


@dataclass
class StandardData:
	report: StandardReport
	data: List[StandardSeries] = field(default_factory = list)
	regions: List[StandardRegion] = field(default_factory = list)
