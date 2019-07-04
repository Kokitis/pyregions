from pathlib import Path
from typing import Iterable, List, Union
from pyregions.dataio import datasets
from infotools import numbertools
from pony.orm import db_session, BindingError
import importlib
from pyregions import standard_definition as sd
from pyregions.database.ponydatabase import sql_entities


class BasicRegionDatabase:
	def __init__(self, filename: Union[str, Path]):
		filename = str(filename)
		try:
			self.database = sql_entities.main_database
			self.database.bind("sqlite", str(filename), create_db = True)  # create_tables
			self.database.generate_mapping(create_tables = True)
		except BindingError:
			sql_entities.main_database = sql_entities.Database()
			importlib.reload(sql_entities)
			self.database = sql_entities.main_database
			self.database.bind("sqlite", str(filename), create_db = True)  # create_tables
			self.database.generate_mapping(create_tables = True)

		self.Region = sql_entities.Region
		self.Report = sql_entities.Report
		self.Series = sql_entities.Series
		self.Scale = sql_entities.Scale
		self.Tag = sql_entities.Tag

	def get_region(self, code = None, **kwargs) -> sql_entities.Region:
		if code:
			kwargs = {'code': code}
		region: sql_entities.Region = self.Region.get(**kwargs)

		return region

	def get_report(self, name: str = None, **kwargs) -> sql_entities.Report:
		if name:
			kwargs = {'name': name}
		report: sql_entities.Report = self.Report.get(**kwargs)
		return report

	def get_series(self, region: str, report: str, code: str) -> sql_entities.Series:
		region_entity = self.get_region(region, asentity = True)
		report_entity = self.get_report(report, asentity = True)
		series = self.Series.get(region = region_entity, report = report_entity, code = code)

		return series

	def get_scale(self, code: str) -> sql_entities.Scale:
		scale = self.Scale.get(code = code)
		return scale

	def check_regions(self, labels: List[str], by_code: bool = True) -> List[str]:
		""" Checks to see if the all the region codes or names in the given list can be found in the database.
			Parameters
			----------
				labels: List[str]
					A list of the region names or codes.
				by_code: bool; default True
					Tells the parser which identifier the given labels represent, coes or names.
		"""
		missing_regions = list()
		for region_label in labels:
			if by_code:
				query = {'code': region_label}
			else:
				query = {'name': region_label}
			region_entity = self.Region.get(**query)
			if region_entity is None:
				missing_regions.append(region_label)
		return missing_regions

	@db_session
	def import_standard_data(self, report: sd.StandardReport, standard_table: List[sd.StandardSeries]):
		"""
			Import data formatted as a standard dataset into the database.
			Import Order
			------------
			regions
			reports
			scale
			units
			series
			notes
			tags
		"""
		# Check for missing regions before attempting to upload data.
		region_codes = [i.region_code for i in standard_table]
		missing_regions = self.check_regions(region_codes)
		if missing_regions:
			message = f"The following regions could not be found in the database: {missing_regions}"
			raise ValueError(message)

		# Make sure the required scale objects are present in the database
		all_scales = [i.scale for i in standard_table]
		# Scales should have already been cleaned so that they are labeled by their standard prefixes.
		missing_scales = [i for i in all_scales if self.get_scale(i) is None]
		if missing_scales:
			message = f"The following scales should be added to the database: {missing_scales}"
			raise ValueError(message)

	# Add the report to the database

	# Add the series to the database

	@db_session
	def import_regions(self, regiondata: Union[Path, Iterable[sd.StandardRegion]]):
		""" Adds a series of regions to the database.
			Parameters
			----------
				regiondata: Union[Path, Iterable[StandardRegion]
					Path to a three-column file with the code, name and type of each region to import. column names should be 'name', 'code', 'type'.
		"""
		if isinstance(regiondata, Path):
			raise NotImplementedError
		else:
			regions = regiondata

		has_valid_codes = [i for i in regions if isinstance(i.code, str)]
		missing_regions = [i for i in has_valid_codes if self.Region.get(code = i.code) is None]

		for item in missing_regions:
			self.Region(name = item.name, code = item.code, type = item.type)


class RegionDatabase(BasicRegionDatabase):
	""" Simple class for preloading the data with commonly-used data."""

	def __init__(self, filename: Path):
		super().__init__(filename)
		self.add_scales()

	# TODO Add more data later, like the weo dataset
	@db_session
	def add_scales(self):
		""" Adds all scales to the database. Since these should not change, adding them now will remove a possible error when importing other data."""
		for scale in numbertools.SCALE:
			code = scale.prefix if scale.prefix else 'unit'
			if self.Scale.get(code = code) is None:
				self.Scale(code = code, multiplier = scale.multiplier)

	def add_namespace_iso(self):
		""" Adds the ISO3 namespace to the database."""
		iso_table = datasets.get_namespace_iso()
		regiondata = list()
		for index, row in iso_table.iterrows():
			region = sd.StandardRegion(code = row['iso3'], name = row['regionName'], type = 'country')
			regiondata.append(region)

		self.import_regions(regiondata)

	def add_namespace_usps(self):
		""" Adds all usps postal codes to the database."""
		usps_table = datasets.get_namespace_usps()

		regiondata = [
			sd.StandardRegion(code = row['usps'], name = row['regionName'], type = row['regionType'])
			for _, row in usps_table.iterrows()
		]

		self.import_regions(regiondata)

	def add_namespace_fips(self):
		""" Adds the fips namespace to the database."""
		raise NotImplementedError
