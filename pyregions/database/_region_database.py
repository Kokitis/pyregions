from ._sql_entities import main_database, Region, Report, Series, Agency, Tag, Scale
from .data_entities import DataAgency, DataRegion, DataReport, DataScale, DataSeries, DataTag
from pony.orm import db_session
from pyregions.standard_table_definition import StandardTable
def get_scale_multiplier(scale_code:str)->float:
	raise NotImplementedError

class RegionDatabase:
	def __init__(self, filename: Union[str, Path]):
		filename = str(filename)
		self.database = main_database
		self.database.bind("sqlite", str(filename), create_db = True)  # create_tables
		self.database.generate_mapping(create_tables = True)

		self.Region = Region
		self.Report = Report
		self.Series = Series
		self.Scale  = Scale
		self.Agency = Agency
		self.Tag = Tag

	def get_region(self, code = None, asentity = False, **kwargs) -> DataRegion:
		if code:
			kwargs = {'code', code}
		region: Region = Region.get(**kwargs)
		if asentity: return region
		return region.to_data()

	def get_report(self, name: str = None, asentity = False, **kwargs) -> DataReport:
		if name:
			kwargs = {'name': name}
		report: Report = Report.get(**kwargs)
		if asentity: return report
		return report.to_data()

	def get_series(self, region: str, report: str, code: str, asentity = False) -> DataSeries:
		region_entity = self.get_region(region, asentity = True)
		report_entity = self.get_report(report, asentity = True)
		series = Series.get(region = region_entity, report = report_entity, code = code)

		if asentity:
			return series
		return series.to_data()

	def get_scale(self, code: str, unit: str, asentity: False) -> DataScale:
		scale = Scale.get(code = code, unit = unit)

		if asentity:
			return scale
		return scale.to_data()

	def insert_scale(self, code:str, unit: str)->Scale:
		multiplier = get_scale_multiplier(code)
		return Scale(code = code, unit = unit, multiplier = multiplier)


	def import_table(self, table: StandardTable, report:DataReport, agency:DataReport) -> bool:

		# Import regions
		for region in table.regions:
			pass

		#import series


		for series in table.data:
			series_scale = series.scale
			series_unit = series.units

			scale_entity = self.Scale.get(code = series_scale, unit  = series_unit)

			if scale_entity is None:
				scale_entity = self.insert_scale(series_scale, series_unit)


