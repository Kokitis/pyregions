
from sqlalchemy import Column, Date, Float, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

# String constrains the length of our str objects. Since Text is unbounded, it is probably preferable.
# However, String may make table operations faster.
# TODO: Evaluate whther it's worth converting some fields to String rather than Text.
EntityBase = declarative_base()

_region_region_code_link_table = Table(
	'regionregioncode', EntityBase.metadata,
	Column('region_id', ForeignKey('regions.id')),
	Column('region_code', ForeignKey('regioncodes.id'))
)

class Namespace(EntityBase):
	__tablename__ = "namespaces"
	id = Column(Integer, primary_key = True)
	name: str = Column(Text)
	codes = relationship("RegionCode", back_populates = "namespace")
	def __repr__(self) -> str:
		s = f"Namespace(name = '{self.name}')"
		return s


class RegionCode(EntityBase):
	__tablename__ = 'regioncodes'
	id = Column(Integer, primary_key = True)
	value: str = Column(Text)
	_namespace_id = Column(Integer, ForeignKey(Namespace.id))
	namespace = relationship("Namespace", back_populates = "codes")
	regions = relationship('Region', secondary = _region_region_code_link_table, back_populates = 'codes')
	def __repr__(self) -> str:
		s = f"RegionCode(value = '{self.value}')"
		return s


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

	name = Column(Text)
	type = Column(Text)
	codes = relationship('RegionCode', secondary = _region_region_code_link_table, back_populates = '')

	# TODO: Add alias


	# TODO: Add alias

	def __repr__(self) -> str:
		string = f"Region(name = '{self.name}', type = '{self.type}')"
		return string

	def series(self):
		raise NotImplementedError


class Report(EntityBase):
	__tablename__ = "reports"
	name = Column(Text, primary_key = True)
	date = Column(Date)
	url = Column(Text)
	agency = Column(Text)
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

	code = Column(Text)
	description = Column(Text)
	name = Column(Text)
	notes = Column(Text)
	units = Column(Text)


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
	code = Column(String(10), primary_key = True)
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
