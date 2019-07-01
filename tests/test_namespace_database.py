from pyregions.namespaces import namespace_database as ndb
import pytest
import importlib
from pony.orm import db_session
import math
from loguru import logger


@pytest.fixture
def empty_namespace(tmp_path) -> ndb.NamespaceDatabase:
	ndb.entities = importlib.reload(ndb.entities)
	logger.debug(tmp_path)
	db = ndb.NamespaceDatabase(tmp_path / "empty_database.sqlite")
	db.database.drop_all_tables(with_all_data = True)
	db.database.create_tables()

	return db


@pytest.fixture
def namespace_database(empty_namespace) -> ndb.NamespaceDatabase:
	with db_session:
		namespace = empty_namespace.Namespace(
			name = "testNamespace",
			url = "testUrl"
		)

		region1 = empty_namespace.Region(
			name = "United States",
			type = "country"
		)
		empty_namespace.Code(
			namespace = namespace,
			region = region1,
			value = "USA"
		)

		region2 = empty_namespace.Region(
			name = "France",
			type = "country"
		)
		empty_namespace.Code(
			namespace = namespace,
			region = region2,
			value = "FRA"
		)

	return empty_namespace


def test_that_the_database_can_be_created():
	ndb.NamespaceDatabase(":memory:")


def test_get_namespace(namespace_database):
	assert namespace_database.get_namespace("ABC") is None
	assert namespace_database.get_namespace("testNamespace").name == "testNamespace"


def test_get_code(namespace_database):
	with db_session:
		assert namespace_database.get_code("testNamespace", "deu") is None
		assert namespace_database.get_code(namespace_database.get_namespace("testNamespace"), "fra").value == "FRA"
		assert namespace_database.get_code("testNamespace", "fra").value == "FRA"


def test_get_region_by_code(namespace_database):
	with db_session:
		namespace = namespace_database.get_namespace("testNamespace")

		assert namespace_database.get_region_from_code("USA", namespace).name == "United States"


def test_namespace_database_import_iso_add_codes(empty_namespace):
	with db_session:
		# Make sure the namespace doesn't already exist.
		assert empty_namespace.get_namespace("ISO 3166-1 alpha-3") is None

		empty_namespace.import_iso()

		ns2 = empty_namespace.get_namespace("ISO 3166-1 alpha-2")
		ns3 = empty_namespace.get_namespace("ISO 3166-1 alpha-3")
		assert ns3 is not None

		assert empty_namespace.get_code(ns3, 'USA').value == 'USA'

		# The soviet union is not an official part of the namespace, but was added manually.
		assert empty_namespace.get_code(ns3, 'SUN').value == 'SUN'

		# Test that the capitalization doesn't matter.
		assert empty_namespace.get_code(ns2, 'gb').value == 'GB'

		# Make sure nan was not accidently added to the database
		assert empty_namespace.get_code(ns3, 'nan') is None

		# Make sure that the three namespaces are separate.
		assert empty_namespace.get_code(ns2, 'usa') is None


def test_namespace_database_import_iso_add_regions(empty_namespace):
	with db_session:
		# Make sure the namespace doesn't already exist.
		assert empty_namespace.get_namespace("ISO 3166-1 alpha-3") is None

		empty_namespace.import_iso()

		ns3 = empty_namespace.get_namespace("ISO 3166-1 alpha-3")
		assert ns3 is not None

		assert empty_namespace.get_code(ns3, 'USA').region.name == 'United States of America'

		# The soviet union is not an official part of the namespace, but was added manually.
		assert empty_namespace.get_code(ns3, 'SUN').region.name == 'Soviet Union'


def test_namespace_database_import_usps_adds_codes(empty_namespace):
	with db_session:
		# Make sure the namespace doesn't already exist.
		assert empty_namespace.get_namespace("ISO 3166-1 alpha-3") is None

		empty_namespace.import_usps()

		ns = empty_namespace.get_namespace("United States Postal Abbreviations")

		assert ns is not None

		assert empty_namespace.get_code(ns, 'USA-TX').value == 'USA-TX'
		assert empty_namespace.get_code(ns, 'USA-PR').value == 'USA-PR'
		assert empty_namespace.get_code(ns, 'USA-DC').value == 'USA-DC'


def test_namespace_database_import_usps_add_regions(empty_namespace):
	with db_session:
		# Make sure the namespace doesn't already exist.
		assert empty_namespace.get_namespace("ISO 3166-1 alpha-3") is None

		empty_namespace.import_usps()

		ns = empty_namespace.get_namespace("United States Postal Abbreviations")

		assert ns is not None

		assert empty_namespace.get_code(ns, 'USA-TX').region.name == 'Texas'
		assert empty_namespace.get_code(ns, 'USA-PR').region.name == 'Puerto Rico'
		assert empty_namespace.get_code(ns, 'USA-DC').region.name == 'District of Columbia'


@pytest.mark.parametrize(
	"value,expected",
	[
		(math.nan, False),
		('usa', True),
		('1234', True),
		(1234, False),
		(str(math.nan), False)
	]
)
def test_is_valid_code(value, expected):
	assert ndb.is_valid_code(value) == expected
