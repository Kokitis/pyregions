import pytest
from pyregions.database.ponydatabase import sql_entities, region_database as rdb
from pyregions import standard_definition as sd
from pony.orm import db_session
import datetime
from loguru import logger
import importlib

@pytest.fixture
def empty_database(tmp_path)->rdb.RegionDatabase:
	rdb.sql_entities = importlib.reload(sql_entities)
	filename = tmp_path / "empty_database.sqlite"
	logger.debug(f"Creating empty database as {filename}")
	region_db = rdb.RegionDatabase(filename)
	region_db.database.drop_all_tables(with_all_data = True)
	region_db.database.create_tables()
	return region_db

@pytest.fixture
def region_database(tmp_path) -> rdb.RegionDatabase:
	rdb.sql_entities = importlib.reload(sql_entities)
	filename = tmp_path / "region_database.sqlite"
	logger.debug(f"Creating region database as {filename}")
	empty_database = rdb.RegionDatabase(filename)
	empty_database.database.drop_all_tables(with_all_data = True)
	empty_database.database.create_tables()
	with db_session:
		region1 = empty_database.Region(
			code = 'TEST1',
			name = 'testregion1',
			type = 'testregion'
		)
		empty_database.Region(
			code = 'TEST2',
			name = 'testregion2',
			type = 'testregion'
		)

		report = empty_database.Report(
			name = 'testReport',
			agency = 'testAgency',
			url = 'http://www.somewebsite.com',
			date = datetime.datetime.now()
		)
		empty_database.add_scales()
		scale = empty_database.get_scale('kilo')
		tag1 = empty_database.Tag(value = 'tag1')
		tag2 = empty_database.Tag(value = 'tag2')
		series = empty_database.Series(
			code = 'S1',
			name = 'testseries1',
			description = 'testdescription',
			notes = '',
			region = region1,
			report = report,
			scale = scale,
			units = 'person',
			years = [2012, 2013, 2014, 2015],
			values = [1, 12, 123, 1234],
			tags = [tag1, tag2]
		)
	return empty_database

def test_database_can_be_created():
	rdb.RegionDatabase(':memory:')

def test_regions_can_be_added_to_the_database(empty_database):
	test_regions = [
		sd.StandardRegion('TE1', 'testregion1', 'testregion'),
		sd.StandardRegion('TE2', 'testregion2', 'testregion'),
		sd.StandardRegion('TE3', 'testregion3', 'testregion')
	]
	with db_session:
		assert empty_database.Region.get(code = 'TE1') is None
		assert empty_database.Region.get(code = 'TE2') is None
		assert empty_database.Region.get(name = 'testregion3') is None

	empty_database.import_regions(test_regions)
	with db_session:
		assert empty_database.Region.get(code = 'TE1') is not None
		assert empty_database.Region.get(code = 'TE1').name == 'testregion1'
		assert empty_database.Region.get(code = 'TE2') is not None
		assert empty_database.Region.get(name = 'testregion3') is not None

def test_regions_can_be_added_to_the_database_if_some_already_exist(empty_database):
	with db_session:
		empty_database.Region(code = 'TE2', name = 'testregion2a', type = 'testregion')
	test_regions = [
		sd.StandardRegion('TE1', 'testregion1', 'testregion'),
		sd.StandardRegion('TE2', 'testregion2b', 'testregion'),
		sd.StandardRegion('TE3', 'testregion3', 'testregion')
	]
	with db_session:
		assert empty_database.Region.get(code = 'TE1') is None
		assert empty_database.Region.get(code = 'TE2').name == 'testregion2a'
		assert empty_database.Region.get(name = 'testregion3') is None

	empty_database.import_regions(test_regions)
	with db_session:
		assert empty_database.Region.get(code = 'TE1') is not None
		assert empty_database.Region.get(code = 'TE1').name == 'testregion1'
		assert empty_database.Region.get(code = 'TE2').name == 'testregion2a'
		assert empty_database.Region.get(name = 'testregion3') is not None

def test_add_scales_to_database(empty_database):
	with db_session:
		empty_database.add_scales()
		result = empty_database.Scale.get(code = 'kilo')
	assert result.code == 'kilo'

def test_import_some_data_into_database(empty_database):
	with db_session:
		region = empty_database.Region(
			code = 'TEST1',
			name = 'testregion1',
			type = 'testregion'
		)

		report = empty_database.Report(
			name = 'testReport',
			agency = 'testAgency',
			url = 'http://www.somewebsite.com',
			date = datetime.datetime.now()
		)
		scale = empty_database.Scale(
			code = 'kilo',
			multiplier = 1000
		)
		tag1 = empty_database.Tag(value = 'tag1')
		tag2 = empty_database.Tag(value = 'tag2')
		series = empty_database.Series(
			code = 'S1',
			name = 'testseries1',
			description = 'testdescription',
			notes = '',
			region = region,
			report = report,
			scale = scale,
			units = 'person',
			years = [2012,2013,2014,2015],
			values = [1,12,123,1234],
			tags = [tag1, tag2]
		)

def test_get_region_by_code(region_database):
	with db_session:
		result = region_database.get_region('TEST2')
	assert result.name == 'testregion2'

def test_get_report_by_name(region_database):
	with db_session:
		result = region_database.get_report('testReport')
	assert result.name == 'testReport'

def test_get_series_by_code(region_database):
	region = 'TEST1'
	report = 'testReport'
	with db_session:
		result = region_database.get_series(region, report, 'S1')
	assert result.name == 'testseries1'

def test_get_scale_by_code(region_database):
	with db_session:
		assert region_database.get_scale('milli').code == 'milli'


def test_add_scales(empty_database):
	with db_session:
		assert empty_database.Scale.get(code = 'mega') is None

		empty_database.add_scales()

		scale = empty_database.Scale.get(code = 'mega')
		assert scale is not None
		assert scale.code == 'mega'

		assert empty_database.Scale.get(code = 'unit') is not None

def test_add_namespace_iso_to_database(empty_database):
	with db_session:
		empty_database.add_namespace_iso()

		assert empty_database.Region.get(code = 'USA') is not None
		assert empty_database.Region.get(code = 'SUN') is not None
		assert empty_database.Region.get(code = 'BRA') is not None

def test_add_usps_codes_to_database(empty_database):
	with db_session:
		# Make sure the database is empty
		assert empty_database.Region.get(code = 'USA-NY') is None
		empty_database.add_namespace_usps()

		assert empty_database.Region.get(code = 'USA-NY') is not None
		assert empty_database.Region.get(code = 'USA-PR') is not None