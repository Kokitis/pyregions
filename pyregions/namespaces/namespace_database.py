from pathlib import Path
from typing import Optional, Union, Any
from pyregions.dataio import datasets
from pony.orm import ObjectNotFound, db_session
from loguru import logger
from . import entities

NAMESPACE_PRIOIRTY = [

]


class BasicNamespaceDatabase:
	def __init__(self, filename: Union[str, Path]):
		self.database = entities.database_object
		self.database.bind("sqlite", str(filename), create_db = True)  # create_tables
		self.database.generate_mapping(create_tables = True)

		self.Namespace = entities.Namespace
		self.Code = entities.Code
		self.Region = entities.Region

	@db_session
	def get_namespace(self, value: Union[str, entities.Namespace]) -> Optional[entities.Namespace]:
		if isinstance(value, str):
			return self.Namespace.get(name = value)
		else: return value

	@db_session
	def get_code(self, namespace: Union[str, entities.Namespace], value: str) -> Optional[entities.Code]:
		namespace_entity = self.get_namespace(namespace)

		try:
			return self.Code[namespace_entity, value.upper()]
		except (ObjectNotFound, ValueError):
			# ObjectNotFound: THe object doesn't exist.
			# ValueError: `namespace_entity` or `value` is None
			return None

	@db_session
	def get_region_from_code(self, code: str, namespace: Union[str, entities.Namespace])->Optional[entities.Region]:
		code_entity = self.get_code(namespace, code)
		if code_entity is not None:
			return code_entity.region


class NamespaceDatabase(BasicNamespaceDatabase):
	"""
		The entities should be imported in this order:
		1. Namespace
		2. Region
		3. Code
	"""

	def __init__(self, filename: Union[str, Path]):
		super().__init__(filename)

	def import_namespace_code(self, namespace: entities.Namespace, region: entities.Region, code: str) -> Optional[entities.Code]:
		# logger.debug(f"import_namespace_code({namespace.name}, {region.name}, {code})")
		if not is_valid_code(code): return None
		code = code.upper()
		result = self.Code(
			namespace = namespace,
			region = region,
			value = code
		)
		return result

	def import_region(self, name: str, region_type: str) -> entities.Region:
		region = self.Region(name = name, type = region_type)
		region.aliases.append(name)
		return region

	def import_iso(self):
		""" ISO numerical codes are optional, so some will be NaN."""
		table = datasets.get_namespace_iso()
		description = "Codes for the representation of names of countries and their subdivisions " \
					  "– Part 1: Country codes[2] defines codes for the names of countries, " \
					  "dependent territories, and special areas of geographical interest."
		namespace_iso3 = self.Namespace(
			name = "ISO 3166-1 alpha-3",
			url = "https://www.iso.org/standard/63545.html",
			description = description,
			wiki = "https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes"
		)
		namespace_iso2 = self.Namespace(
			name = "ISO 3166-1 alpha-2",
			url = "https://www.iso.org/standard/63545.html",
			description = description,
			wiki = "https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes"
		)
		namespace_ison = self.Namespace(
			name = "ISO 3166-1 numeric",
			url = "https://www.iso.org/standard/63545.html",
			description = description,
			wiki = "https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes"
		)

		for index, row in table.iterrows():
			region = self.import_region(row['regionName'], row['regionType'])

			# Each code is optional, although most should be present.

			self.import_namespace_code(namespace_iso2, region, row['iso2'])
			self.import_namespace_code(namespace_iso3, region, row['iso3'])
			self.import_namespace_code(namespace_ison, region, row['ison'])

	def import_usps(self):
		table = datasets.get_namespace_usps()
		description = "US Postal abbreviations are based on iso-3166 subdivision codes."

		ns = self.Namespace(
			name = "United States Postal Abbreviations",
			url = "https://www.stateabbreviations.us",
			description = description,
			wiki = "https://en.wikipedia.org/wiki/List_of_U.S._state_abbreviations"
		)
		# Since all of these regions are US states, territories, etc, they should be added under 'USA'
		usa = self.get_region_from_code("USA", "ISO 3166-1 alpha-3")
		if usa is None:
			usa = self.import_region("United States", "country")

		for index, row in table.iterrows():
			region = self.import_region(row['regionName'], row['regionType'])
			region.parent = usa

			# Ignore iso subdivision codes for now.
			self.import_namespace_code(ns, region, row['usps'])


def is_valid_code(value: Any) -> bool:
	if isinstance(value, str):
		return value != 'nan'
	else:
		# Probably nan
		return False
