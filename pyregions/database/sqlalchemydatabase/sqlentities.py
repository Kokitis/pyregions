from sqlalchemy import Column, Date, Float, Integer, String, Text, ForeignKey, Table, Numeric, ARRAY
from sqlalchemy.orm import relationship
from typing import Iterable, Collection, List
from sqlalchemy.ext.declarative import declarative_base
import datetime

# String constrains the length of our str objects. Since Text is unbounded, it is probably preferable.
# However, String may make table operations faster.
# TODO: Evaluate whther it's worth converting some fields to String rather than Text.
EntityBase = declarative_base()


class Namespace(EntityBase):
	__tablename__ = "namespace"
	id: int = Column(Integer, primary_key = True)
	name: str = Column(Text)
	url: str = Column(Text)
	codes: Iterable["RegionCode"] = relationship("RegionCode", back_populates = "namespace")

	def __repr__(self) -> str:
		s = f"Namespace(name = '{self.name}')"
		return s


class RegionCode(EntityBase):
	__tablename__ = 'regioncode'
	id: int = Column(Integer, primary_key = True)
	value: str = Column(Text)

	# Establish a relationsship from RegionCode to Namespace
	namespace_id: int = Column(Integer, ForeignKey("namespace.id"))
	namespace: "Namespace" = relationship("Namespace", back_populates = "codes")

	# Establish a relationship with a Region
	region_id: int = Column(Integer, ForeignKey("region.id"))
	region: "Region" = relationship('Region', back_populates = 'codes')

	def __repr__(self) -> str:
		s = f"RegionCode(value = '{self.value}')"
		return s


class Region(EntityBase):
	__tablename__ = 'region'

	id: int = Column(Integer, primary_key = True)

	name: str = Column(Text)
	type: str = Column(Text)

	# Establish relationship with RegionCode
	codes: Iterable["RegionCode"] = relationship("RegionCode", back_populates = "region")

	# Establish relationship with `series`
	series: Iterable["Series"] = relationship("Series", back_populates = "region")

	# TODO: Add aliases

	def __repr__(self) -> str:
		string = f"Region(name = '{self.name}', type = '{self.type}')"
		return string


class Report(EntityBase):
	__tablename__ = "report"
	id: int = Column(Integer, primary_key = True)
	name: str = Column(Text)
	date: datetime.date = Column(Date)
	url: str = Column(Text)
	agency: str = Column(Text)
	# Used to indicate the day of year that the dataset corresponds to.
	# Ex. census data starts mid-year.
	day_of_year: int = Column(Integer)

	# Establish relationship with Series
	series: Iterable["Series"] = relationship("Series", back_populates = "report")

	def __repr__(self) -> str:
		s = f"Report(date = '{self.date}', name = '{self.name}', agency = '{self.agency}')"
		return s


class Series(EntityBase):
	__tablename__ = "series"
	id: int = Column(Integer, primary_key = True)

	code: str = Column(Text)
	description: str = Column(Text)
	name: str = Column(Text)
	notes: str = Column(Text)
	units: str = Column(Text)

	_x: str = Column(Text)
	_y: str = Column(Text)

	# Establish relationship with Report
	report_id: str = Column(String, ForeignKey("report.id"))
	report: "Report" = relationship("Report", back_populates = "series")

	region_id: int = Column(Integer, ForeignKey("region.id"))
	region: "Region" = relationship("Region", back_populates = "series")

	scale_id: int = Column(Integer, ForeignKey("scale.code"))
	scale: "Scale" = relationship("Scale", back_populates = "series")

	@property
	def x(self):
		return self._unpack_list(self._x, int)

	@x.setter
	def x(self, values: Iterable[int]):
		self._x = self._pack_list(values)

	@property
	def y(self) -> List[float]:
		return self._unpack_list(self._y, float)

	@y.setter
	def y(self, values: Iterable[float]):
		self._y = self._pack_list(values)

	def __repr__(self) -> str:
		s = f"Series(code = '{self.code}', name = '{self.name}', units = '{self.units}')"
		return s

	@staticmethod
	def _unpack_list(value: str, dtype) -> List:
		""" Converts a string of elements into a list of values"""
		vs = [dtype(i) for i in value.split('|')]
		return vs

	@staticmethod
	def _pack_list(iterable: Iterable) -> str:
		v = "|".join([str(i) for i in iterable])
		return v

	def tags(self):
		raise NotImplementedError

	def years(self):
		raise NotImplementedError

	def values(self):
		raise NotImplementedError


class Scale(EntityBase):
	__tablename__ = "scale"
	code: str = Column(String(10), primary_key = True)
	multiplier: float = Column(Float)

	series: Collection["Series"] = relationship("Series", back_populates = "scale")

	def __repr__(self) -> str:
		s = f"Scale(code = {self.code}, multiplier = {self.multiplier})"
		return s


if __name__ == "__main__":
	from sqlalchemy import create_engine
	from sqlalchemy.orm import sessionmaker

	engine = create_engine('sqlite:///:memory:')

	EntityBase.metadata.create_all(engine)
	Session = sessionmaker(bind = engine)  # This is a class, not an object
	session = Session()
	testnamespace = Namespace(name = 'test')

	code1 = RegionCode(value = 'USA', namespace = testnamespace)
	code2 = RegionCode(value = 'SUN', namespace = testnamespace)
	# testnamespace.codes = [code1, code2]
	session.add(testnamespace)
	session.add(code1)
	session.add(code2)
	session.commit()
	print(testnamespace)
	print(testnamespace.codes)
