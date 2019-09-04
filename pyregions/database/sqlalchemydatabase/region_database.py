from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional, Iterable, Tuple, Union
import datetime

try:
	from . import sqlentities as sql
except ModuleNotFoundError:
	import sqlentities as sql


class BaseDatabase:
	def __init__(self, filename = None):
		if filename is None:
			self.filename = ':memory:'
		else:
			self.filename = filename

		self.session = self.create_database(self.filename)

	@staticmethod
	def create_database(filename: Optional[str]):
		""" Creates an sqlite database."""
		engine = create_engine(f'sqlite:///{filename}')

		sql.EntityBase.metadata.create_all(engine)
		Session = sessionmaker(bind = engine)  # This is a class, not an object
		session = Session()

		return session

	def get_region_from_code(self, code: str) -> Optional[sql.Region]:
		region_code = self.session.query(sql.RegionCode.value == code).first()
		return region_code.region

	def get_report(self, name: str) -> Optional[sql.Report]:
		report = self.session.query(sql.Report.name == name).first()
		return report

	def get_scale(self, value:Union[str, float, None]) -> Optional[sql.Scale]:
		"""Attempts to find a scale based on Scale.code if a value is passed, or by Scale.multiplier if value is a float."""
		if isinstance(value, str):
			scale = self.session.query(sql.Scale.code == value).first()
		elif isinstance(value, float):
			scale = self.session.query(sql.Scale.multiplier == value).first()
		else:
			scale = None
		return scale

	def get_series(self) -> sql.Series:
		raise NotImplementedError

	def add_region(self, name: str, type: str):
		region = sql.Region(
			name = name,
			type = type
		)
		self.session.add(region)
		return region

	def add_report(self, name: str, date: datetime.date, url: str, agency: str, day_of_year: Optional[int] = None):
		if day_of_year is None:
			day_of_year = 0
		else:
			day_of_year = int(day_of_year)
		region = sql.Report(
			name = name,
			date = date,
			url = url,
			agency = agency,
			day_of_year = day_of_year
		)

		self.session.add(region)

		return region

	def add_namespace(self, name: str, url: str) -> sql.Namespace:
		namespace = sql.Namespace(name = name, url = url)
		self.session.add(namespace)
		return namespace

	def add_regioncode(self, value: str, region: sql.Region, namespace: sql.Namespace) -> sql.RegionCode:
		region_code = sql.RegionCode(
			value = value,
			region = region,
			namespace = namespace
		)
		self.session.add(region_code)
		return region_code

	def add_scales(self):
		""" It's simpler to add these all at once."""
		pass

	def add_series(self, name: str, code: str, description: str, notes: str, units: str,
				   values: Iterable[Tuple[int, float]], report:sql.Report, region:sql.Region, scale:sql.Scale) -> sql.Series:
		series = sql.Series(
			name = name,
			code = code,
			description = description,
			notes = notes,
			units = units,

			report = report,
			region = region,
			scale = scale
		)

		x, y = zip(*values)
		series.x = x
		series.y = y

		self.session.add(series)

		return series

	def import_report(self, report):
		""" Adds a report which has been formatted using the standardized API format."""