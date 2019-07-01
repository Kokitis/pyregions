import os
SHAPEFILE_FOLDER = os.path.join(os.path.dirname(__file__), 'shapefiles')
from typing import *
DEFAULT_MAP_PARAMETERS = {
	'global':                 {
		'projection':          None,
		'regionType':          'country',
		'filename':            os.path.join(SHAPEFILE_FOLDER, 'ne_50m_admin_0_countries'),
		'regionCodeColumn':    'ISO_A3',
		'regionCodeNamespace': 'ISO3',
		'data':                {
			'regionPopulation': '',
			'regionTotalArea':  ''
		}
	},
	'global subregions':      {
		'regionType':          'subregion',
		'projection':          None,
		'filename':            os.path.join(SHAPEFILE_FOLDER, 'ne_10m_admin_1_states_provinces.zip'),
		'regionCodeColumn':    "iso_3166_2",
		'regionNameColumn':    'name',
		'regionCodeNamespace': 'ISO2',
		'geometryColumn':      'geometry'
	},
	'states':                 {
		'regionType':          'state',
		'projection':          'eqdc',
		'filename':            os.path.join(SHAPEFILE_FOLDER, 'cb_2016_us_state_500k.zip'),
		'geometryColumn':      'geometry',
		'regionCodeColumn':    'STUSPS',
		'regionCodeNamespace': "USPS",
		'regionNameColumn':    'NAME',
		'data':                {
			'regionWaterAreaColumn': 'AWATER',
			'regionLandAreaColumn':  'ALAND'
		},
		'metadata':            {  # Used to annotate the map.
			'shapefileSource': 'US Census Bureau'
		}
	},
	'counties':               {
		'regionType':          'county',
		'projection':          'eqdc',
		'filename':            os.path.join(SHAPEFILE_FOLDER, 'cb_2016_us_county_500k.zip'),
		'geometryColumn':      'geometry',
		'regionCodeColumn':    'FIPS',
		'regionCodeNamespace': 'FIPS',
		'regionNameColumn':    'NAME',
		'data':                {
			'regionWaterAreaColumn': 'AWATER',
			'regionLandAreaColumn':  'ALAND'
		}
	},
	'congressional district': {
		'regionType':       'congressional district',
		'projection':       None,
		'filename':         os.path.join(SHAPEFILE_FOLDER, 'cb_2016_us_cd115_500k.zip'),
		'geometryColumn':   'geometry',
		'regionCodeColumn': 'FIPS',
		'regionNameColumn': 'NAME',
		'data':             {
			'regionWaterAreaColumn': 'AWATER',
			'regionLandAreaColumn':  'ALAND'
		}
	},
	'nuts2013':               {
		'regionType':       'nuts2013',
		'projection':       None,
		'filename':         os.path.join(SHAPEFILE_FOLDER),
		'geometryColumn':   'geometry',
		'regionCodeColumn': 'STUSPS',
		'regionNameColumn': 'NAME',
	}
}

DEFAULT_PROJECTION_PARAMETERS = {
	'usa':    {
		'eqdc': {
			'proj4':      {
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
			},
			'bounds':     {
				'lat': (25, 50),
				'lon': (-125, -67)
			},
			'dimensions': {
				'width':  (-2500000, 2500000),
				'height': (-1500000, 1500000)
			}
		}
	},
	'global': {
		'robin': {
			'proj4':      {
				'proj':  'robin',
				'lon_0': 0
			},
			'bounds':     None,
			'dimensions': None
		}
	}
}
def getDefaultGeometryTableParameters(kind: str) -> Dict[str, Optional[Union[Dict, str]]]:
	"""

	Parameters
	----------
	kind: {'global', 'usa', 'global subregions', 'states', 'counties', 'congressional district}

	Returns
	-------
		dict
			* 'regionType':
			* 'projection':
			* 'filename':
			* 'geometryColumn':
			* 'regionCodeColumn':
			* 'regionNameColumn':
			* 'regionCodeNamespace':
			* 'data"
			* 'metadata'
	"""

	if kind in DEFAULT_MAP_PARAMETERS:
		parameters = DEFAULT_MAP_PARAMETERS[kind]
	else:
		message = "'{}' is not a valid map type. Expected one of {}".format(kind, sorted(
			DEFAULT_MAP_PARAMETERS.keys()))
		raise ValueError(message)

	parameters['projection'] = parameters.get('projection')

	return parameters


def getProjectionParameters(region: str, projection: str):
	"""

	Parameters
	----------
	region
	projection

	Returns
	-------
	dict
		* 'proj4':
		* 'bounds':
		* 'dimensions':
	"""
	if region in {'usa', 'states', 'counties', 'census tracts', 'congressional districts'}:
		region = 'usa'


	if region in DEFAULT_PROJECTION_PARAMETERS and projection in DEFAULT_PROJECTION_PARAMETERS[region]:
		return DEFAULT_PROJECTION_PARAMETERS[region][projection]
	else:
		return dict()