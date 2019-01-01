from pony.orm import Optional, PrimaryKey, Required, Set, Database
from .data_entities import DataRegion, DataTag, DataSeries, DataScale, DataReport, DataAgency
from typing import List
import datetime

main_database = Database()


class Region(main_database.Entity):
	entity_type = 'region'
	code: str = PrimaryKey(str)
	name: str = Required(str)  # PrimaryKey(str)
	type: str = Required(str)
	series: List['Series'] = Set('Series')

	def to_data(self) -> DataRegion:
		return DataRegion(
			code = self.code,
			name = self.name,
			type = self.type,
			series = []
		)


class Report(main_database.Entity):
	entity_type = 'report'

	date: datetime.datetime = Required(datetime.datetime)
	name: str = PrimaryKey(str)
	url: str = Required(str)
	agency: 'Agency' = Required('Agency')
	series: List['Series'] = Set('Series')

	def to_data(self) -> DataReport:
		return DataReport(
			date = self.date,
			name = self.name,
			url = self.url,
			agency = self.agency.to_dict(),
			series = [i.code for i in self.series]
		)


class Series(main_database.Entity):
	entity_type = 'series'
	code: str = Required(str)
	description: str = Optional(str)
	name: str = Required(str)
	notes: str = Optional(str)

	region: Region = Required(Region)
	report: Report = Required(Report)
	scale: 'Scale' = Required('Scale')
	tags: List['Tag'] = Set('Tag')
	PrimaryKey(region, report, code)

	def to_data(self) -> DataSeries:
		return DataSeries(
			code = self.code,
			name = self.name,
			description = self.description,
			notes = self.notes,
			region = self.region.to_dict(),
			report = self.report.to_dict(),
			scale = self.scale.to_dict(),
			tags = [i.value for i in self.tags]
		)


class Scale(main_database.Entity):
	code: str = Required(str)
	unit: str = Required(str)
	multiplier: float = Required(float)
	PrimaryKey(code, unit)
	def to_data(self)->DataScale:
		return DataScale(
			code = self.code,
			unit = self.unit,
			multiplier = self.multiplier
		)


class Agency(main_database.Entity):
	entity_type = 'agency'
	name: str = PrimaryKey(str)
	reports: List[Report] = Set(Report)
	url = Optional(str)

	def to_data(self)->DataAgency:
		return DataAgency(
			name = self.name,
			reports = [i.to_data() for i in self.agency]
		)

class Tag(main_database.Entity):
	entity_type = 'tag'
	value: str = PrimaryKey(str)
	series: List[Series] = Set(Series)
