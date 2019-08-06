from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional, Iterable, Tuple
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

	def get_region(self, code: str) -> sql.Region:
		pass

	def get_report(self, name: str) -> sql.Report:
		raise NotImplementedError

	def get_scale(self) -> sql.Scale:
		raise NotImplementedError

	def get_series(self) -> sql.Series:
		raise NotImplementedError

	def add_region(self, name: str, type: str):
		region = sql.Region(
			name = name,
			type = type
		)
		self.session.add(region)
		return region

	def add_report(self, name: str, date: datetime.datetime, url: str, agency: str, day_of_year: Optional[int] = None):
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

	def add_series(self, code: str, description: str, name: str, notes: str, units: str, values: Iterable[Tuple[int,float]])->sql.Series:
		series = sql.Series(
			name = name,
			code = code,
			description = description,
			notes = notes,
			units = units
		)