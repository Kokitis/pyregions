import pytest
import datetime
from pyregions.database.sqlalchemydatabase.region_database import BaseDatabase, sql
from sqlalchemy.orm import exc


@pytest.fixture
def empty_basedatabase() -> BaseDatabase:
	db = BaseDatabase()
	return db


def test_empty_database_is_empty(empty_basedatabase):
	result = empty_basedatabase.session.query(sql.Region.name == "Japan").first()
	assert result is None
	with pytest.raises(exc.NoResultFound):
		empty_basedatabase.session.query(sql.Region.name == "Japan").one()


def test_add_region_to_database(empty_basedatabase):
	region_name = 'Japan'
	region_type = "country"

	empty_basedatabase.add_region(region_name, region_type)
	# Try querying for the region
	for instance in empty_basedatabase.session.query(sql.Region).order_by(sql.Region.id):
		assert instance.name == region_name
		assert instance.type == region_type


def test_add_namespace_to_database(empty_basedatabase):
	namespace_name = "ISO"
	namespace_url = "testUrl"

	empty_basedatabase.add_namespace(namespace_name, namespace_url)

	# There should only be one instance in the database.
	for instance in empty_basedatabase.session.query(sql.Namespace).order_by(sql.Namespace.id):
		assert instance.name == namespace_name
		assert instance.url == namespace_url


def test_add_region_code_to_database(empty_basedatabase):
	region_name = "Japan"
	region_type = "country"

	namespace_name = "ISO"
	namespace_url = "testUrl"

	code = "JPN"

	namespace = empty_basedatabase.add_namespace(namespace_name, namespace_url)
	region = empty_basedatabase.add_region(region_name, region_type)

	empty_basedatabase.add_regioncode(code, region, namespace)

	for instance in empty_basedatabase.session.query(sql.RegionCode).order_by(sql.RegionCode.id):
		assert instance.value == code
		assert instance.region == region
		assert instance.namespace == namespace

		# Test to make sure the other attributes are linked.
		assert instance.region.name == region_name
		assert instance.namespace.url == namespace_url


def test_add_report_to_database(empty_basedatabase):
	report_name = "testReport"
	report_date = datetime.date(2019, 2, 11)
	report_url = "testUrl"
	report_agency = "testAgency"

	empty_basedatabase.add_report(report_name, report_date, report_url, report_agency)

	for instance in empty_basedatabase.session.query(sql.Report).order_by(sql.Report.id):
		assert instance.agency == report_agency
		assert instance.date == datetime.date(2019, 2, 11)

def test_add_series_to_database(empty_basedatabase):
	report_name = "testReport"
	report_date = datetime.date(2019, 2, 11)
	report_url = "testUrl"
	report_agency = "testAgency"

	region_name = "Japan"
	region_type = "country"

	series_name = "Population"
	series_code = "POP"
	series_description = "testDescription"
	series_notes = "testNotes"
	series_units = "Persons"

	report = empty_basedatabase.add_report(report_name, report_date, report_url, report_agency)
	region = empty_basedatabase.add_region(region_name, region_type)
	scale = empty_basedatabase.add_


	values = [
		(1985, 121048923), (1990, 123611167), (1995, 125570246), (2000, 126925843),
		(2005, 127767994), (2010, 128057352), (2015, 127094745), (2019, 126317000)
	]

	series = empty_basedatabase.add_series(
		name = series_name,
		code = series_code,
		description = series_description,
		notes = series_notes,
		units = series_units,
		values = values,
		report = report,
		region = region,
		scale = scale
	)

	assert series.x == [1985, 1990, 1995, 2000, 2005, 2010, 2015, 2019]
	assert series._x == "1985|1990|1995|2000|2005|2010|2015|2019"


