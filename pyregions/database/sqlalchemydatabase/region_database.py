from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional

try:
	import sqlentities
except:
	from . import sqlentities


class BaseDatabase:
	def __init__(self, filename = None):
		if filename is None:
			self.filename = ':memory:'
		else:
			self.filename = filename

		self.session = self.create_database(self.filename)

	def create_database(self, filename: Optional[str]):
		""" Creates an sqlite database."""
		engine = create_engine(f'sqlite:///{filename}')

		sqlentities.EntityBase.metadata.create_all(engine)
		Session = sessionmaker(bind = engine)  # This is a class, not an object
		session = Session()

		return session

	def get_region(self, code: str) -> sqlentities.Region:
		pass

	def get_report(self, name: str) -> sqlentities.Report:
		raise NotImplementedError

	def get_scale(self) -> sqlentities.Scale:
		raise NotImplementedError

	def get_series(self) -> sqlentities.Series:
		raise NotImplementedError
