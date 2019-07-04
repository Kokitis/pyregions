import datetime
from pyregions.database import data_entities
from typing import List
import pandas
from pony.orm import Database, FloatArray, IntArray, Optional, PrimaryKey, Required, Set

main_database = Database()


class Region(main_database.Entity):
	entity_type = 'region'
	code: str = PrimaryKey(str)
	name: str = Required(str)  # PrimaryKey(str)
	type: str = Required(str)
	series: List['Series'] = Set('Series')

	def load(self) -> data_entities.DataRegion:
		r = data_entities.DataRegion(
			code = self.code,
			name = self.name,
			type = self.type
		)

class Report(main_database.Entity):
	entity_type = 'report'
	date: datetime.datetime = Required(datetime.datetime)
	name: str = PrimaryKey(str)
	url: str = Required(str)
	agency: str = Required(str)
	series: List['Series'] = Set('Series')
	day_of_year:int = Optional(int) # Used to indicate the day of year that the dataset corresponds to. Ex. census data starts mid-year.



class Series(main_database.Entity):
	entity_type = 'series'
	code: str = Required(str)
	description: str = Optional(str)
	name: str = Required(str)
	notes: str = Optional(str)

	region: Region = Required(Region)
	report: Report = Required(Report)
	scale: 'Scale' = Required('Scale')
	units: str = Required(str)
	tags: List['Tag'] = Set('Tag')
	PrimaryKey(report, region, code)
	years: List[int] = Required(IntArray)
	values: List[float] = Required(FloatArray)

	def load(self)->data_entities.DataSeries:
		s = data_entities.DataSeries(
			primarykey = (self.report.name, self.region.code, self.code),
			code = self.code,
			description = self.description,
			name = self.name,
			notes = self.notes,

			region = self.region.load(),
			report = self.report.todict(),
			scale = self.scale,
			units = self.units,
			tags = [i.value for i in self.tags],
			data = pandas.Series(self.values, index = self.years)
		)
		return s


class Scale(main_database.Entity):
	code: str = PrimaryKey(str)
	#unit: str = Required(str) # Replaces the old 'Unit' class
	multiplier: float = Required(float)

	series: str = Set(Series)


class Tag(main_database.Entity):
	entity_type = 'tag'
	value: str = PrimaryKey(str)
	series: List[Series] = Set(Series)


