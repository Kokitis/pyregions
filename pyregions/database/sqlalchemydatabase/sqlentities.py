from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

EntityBase = declarative_base()


class Namespace(EntityBase):
	__tablename__ = "namespaces"
	name: str = Column(String)

	def __repr__(self) -> str:
		s = f"Namespace(name = '{self.name}')"
		return s


class RegionCode(EntityBase):
	__tablename__ = 'regioncodes'
	id = Column(Integer, primary_key = True)
	value: str = Column(String)

	def __repr__(self) -> str:
		s = f"RegionCode(value = '{self.value}')"
		return s


class Region(EntityBase):
	__tablename__ = 'regions'

	id = Column(Integer, primary_key = True)
	name = Column(String)
	type = Column(String)

	# TODO: Add alias

	def __repr__(self) -> str:
		string = f"Region(name = '{self.name}', type = '{self.type}')"
		return string

	def series(self):
		raise NotImplementedError


class Report(EntityBase):
	__tablename__ = "reports"
	name = Column(String, primary_key = True)
	date = Column(DateTime)
	url = Column(String)
	agency = Column(String)
	# Used to indicate the day of year that the dataset corresponds to.
	# Ex. census data starts mid-year.
	day_of_year = Column(Integer)

	def __repr__(self) -> str:
		s = f"Report(date = '{self.date}', name = '{self.name}', agency = '{self.agency}')"
		return s

	def series(self):
		raise NotImplementedError


class Series(EntityBase):
	__tablename__ = "series"
	id = Column(Integer, primary_key = True)
	code = Column(String)
	description = Column(String)
	name = Column(String)
	notes = Column(String)
	units = Column(String)

	def __repr__(self) -> str:
		s = f"Series(code = '{self.code}', name = '{self.name}', units = '{self.units}')"
		return s

	def region(self):
		raise NotImplementedError

	def report(self):
		raise NotImplementedError

	def scale(self):
		raise NotImplementedError

	def tags(self):
		raise NotImplementedError

	def years(self):
		raise NotImplementedError

	def values(self):
		raise NotImplementedError


class Scale(EntityBase):
	__tablename__ = "scale"
	code = Column(String, primary_key = True)
	multiplier = Column(Float)

	def __repr__(self) -> str:
		s = f"Scale(code = {self.code}, multiplier = {self.multiplier})"
		return s

	def series(self):
		raise NotImplementedError


if __name__ == "__main__":
	from sqlalchemy import create_engine
	from sqlalchemy.orm import sessionmaker

	engine = create_engine('sqlite:///:memory:')

	EntityBase.metadata.create_all(engine)
	Session = sessionmaker(bind = engine)  # This is a class, not an object
	session = Session()
	testregion = Region(code = 'USA', name = 'US', type = 'Country')

	session.add(testregion)
	result = session.query(Region).filter_by(code = 'USA').first()
	print(result)
