from pathlib import Path
from pytools.datatools import dataclass
from dataclasses import asdict, field

from typing import List, Tuple, Union, Dict, Optional
import pandas
import math


def to_number(value) -> float:
	try:
		v = float(value)
	except ValueError:
		v = math.nan

	return v

@dataclass
class StandardSeries:
	region_name: str
	region_code: str
	series_name: str
	series_code: str
	series_scale: str
	series_description: str
	series_notes: str
	series_units: str
	series_tags: List[str]
	series_values: List[Tuple[int, float]]

	def to_dict(self) -> Dict[str, Union[str, List]]:
		return asdict(self)

	def to_row(self)->Dict[Union[int, str], Union[str, float]]:
		d = self.to_dict()

		d.update(d.pop('series_values'))
		return d

@dataclass  # For clarity
class RequiredColumns:
	region_code_column: str = 'regionCode'
	region_name_column: str = 'regionName'
	series_code_column: str = 'seriesCode'
	series_name_column: str = 'seriesName'
	series_note_column: str = 'seriesNotes'
	series_scale_column: str= 'seriesScale'
	series_units_column: str= 'seriesUnits'
	series_description_column: str = 'seriesDescription'
	series_tag_column: Optional[str] = 'seriesTags'

	def find_missing_columns(self, columns:List[str])->Optional[List[str]]:
		missing_columns = list()
		for name, value in self.items():
			if value not in columns and name not in ['series_tag_column', "series_note_column"]:
				missing_columns.append(value)

		if len(missing_columns) > 0:
			message = "The following columns are missing: " + str(missing_columns)
			raise ValueError(message)
@dataclass
class StandardTable:
	data: List[StandardSeries] = field(default_factory = list)

	def save(self, path: Path) -> Path:
		table = [i.to_dict() for i in self.data]

		pandas.DataFrame(table).to_excel(str(path))
		return path

	def to_string(self)->str:
		t = pandas.DataFrame([i.to_row() for i in self.data])
		return t.to_string()





