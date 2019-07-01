from pathlib import Path
from typing import Dict, Union
import fiona
import geopandas
from geopandas.plotting import plot_dataframe
import matplotlib.pyplot as plt
import dataio

DATA_FOLDER = Path(__file__).parent / "data"
shapefiles_folder = DATA_FOLDER / "shapefiles"


def _apply_plot_formatting(ax: plt.Axes) -> plt.Axes:
	tick_parameters = {
		'axis':        'both',
		'which':       'both',
		'bottom':      False,
		'top':         False,
		'left':        False,
		'right':       False,
		'labelbottom': False,
		'labelleft':   False,
		'labelright':  False
	}
	plt.tick_params(**tick_parameters)
	return ax


def _apply_region_parameters(ax:plt.Axes, name: str)->plt.Axes:
	if name in ['usa']:
		projection_parameters = {
			'bounds':     {
				'lat': (25, 50),
				'lon': (-125, -67)
			},
			'dimensions': {
				'width':  (-2500000, 2500000),
				'height': (-1500000, 1500000)
			}
		}
	elif name == 'county':
		projection_parameters = {
			'bounds': {
				'lat': (25, 50),
				'lon': (-125, -67)
			}
		}

	else:
		projection_parameters = {}

	dimension_boundaries = projection_parameters.get('dimensions')
	map_boundaries = projection_parameters.get('bounds')
	if dimension_boundaries:
		y_limit = dimension_boundaries['height']
		x_limit = dimension_boundaries['width']
	elif map_boundaries:
		y_limit = map_boundaries['lat']
		x_limit = map_boundaries['lon']

		height = abs(max(y_limit) - min(y_limit))
		width = abs(max(x_limit) - min(x_limit))

		#plot_parameters['figsize'] = (width, height)
	else:
		x_limit = y_limit = None

	if x_limit:
		ax.set_xlim(x_limit)
	if y_limit:
		ax.set_ylim(y_limit)


def geoplot(data: Dict[str, str], name: str):
	"""

	Parameters
	----------
	data: Dict[str,str]
		Maps region codes to colors.
	name

	Returns
	-------

	"""
	default_color = '#333333'
	geometry = dataio.load_geometry(name)

	geometry['regionColor'] = [data.get(i, default_color) for i in geometry['regionCode'].tolist()]

	fig, ax = plt.subplots(figsize = (20, 10))

	groups = geometry.groupby(by = 'regionColor')
	for color, group in groups:
		plot_dataframe(group, color = color, ax = ax)
	ax = _apply_plot_formatting(ax)
	ax = _apply_region_parameters(ax, name)


if __name__ == "__main__":
	data = {
		'42019': '#FF0000',
	}
	geoplot(data, 'county')
	plt.show()
