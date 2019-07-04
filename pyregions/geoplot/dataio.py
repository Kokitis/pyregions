from typing import Union
from pathlib import Path
import geopandas
import fiona

DATA_FOLDER = Path(__file__).parent / "data"
shapefiles_folder = DATA_FOLDER / "shapefiles"


def read_geometry(filename: Union[str, Path]) -> geopandas.GeoDataFrame:
	filename = Path(filename)
	if filename.suffix == '.zip':
		with fiona.Collection(filename, vsi = 'zip') as f:
			geometry_table = geopandas.GeoDataFrame.from_features(f, crs = f.crs)
	else:
		geometry_table = geopandas.read_file(filename)
	return geometry_table


def _load_county_geometry() -> geopandas.GeoDataFrame:
	""" Reads country shapefiles into a GeoDataFrame"""
	filename = shapefiles_folder / "cb_2016_us_county_500k"
	table = read_geometry(filename)

	table['regionCode'] = [f"{i:>02}{j:>03}" for i, j in zip(table['STATEFP'].values, table['COUNTYFP'].values)]
	return table


def _load_congressional_district() -> geopandas.GeoDataFrame:
	filename = shapefiles_folder / ""
	geometry_table = read_geometry(filename)
	geometry_table['FIPS'] = [
		"{:>02}{:>02}".format(i, j)
		for i, j in zip(
			geometry_table['STATEFP'].values, geometry_table['CDFP'].values
		)
	]
	return geometry_table


def _load_world_geometry() -> geopandas.GeoDataFrame:
	""" Reads the world shapefile into a GeoDataFrame"""
	filename = shapefiles_folder / "ne_50m_admin_0_countries"
	table = read_geometry(filename)
	table['regionCode'] = table['ISO_A3']
	proj4_parameters = {
		'proj':  'robin',
		'lon_0': 0
	}
	table = table.to_crs(proj4_parameters)
	return table


def _load_state_geometry() -> geopandas.GeoDataFrame:
	filename = shapefiles_folder / "cb_2016_us_state_500k"

	table = read_geometry(filename)
	table['regionCode'] = table['STUSPS']

	projection = {
		'proj':    'eqdc',
		'lon_0':   -96,
		'lat_0':   39,
		'lat_1':   33,
		'lat_2':   45,
		'x_0':     0,
		'y_0':     0,
		'datum':   'NAD83',
		'units':   'm',
		'no_defs': True
	}
	table = table.to_crs(projection)

	return table


def load_geometry(name: str) -> geopandas.GeoDataFrame:
	"""
		Loads the shapefile corresponding to the region from 'named'
	Parameters
	----------
	name: {'world', 'usa', 'county', 'nuts'}

	Returns
	-------
	geopandas.GeoDataFrame
	"""
	if name == 'world':
		table = _load_world_geometry()
	elif name == 'county':
		table = _load_county_geometry()
	elif name in ['usa', 'states']:
		table = _load_state_geometry()
	else:
		message = f"Not an available region: '{name}'"
		raise ValueError(message)
	return table
