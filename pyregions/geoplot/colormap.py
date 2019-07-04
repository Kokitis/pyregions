import math
import matplotlib.patches as mpatches

from typing import *

Number = Union[int, float]

from pprint import pprint
import seaborn
from collections import namedtuple

ColorPair = namedtuple('ColorPair', ['value', 'color'])

common_palettes = {
	'percent': {
		'values': list(range(0, 101, 10)),
		'upper': 100,
		'lower': 0,
	}
}

class ColorBin:
	def __init__(self, lower: Number, upper: Number, color: str):
		self.color: str = color
		self.lower: Number = lower
		self.upper: Number = upper

	def __contains__(self, value: Number) -> bool:
		return self.lower <= value < self.upper

	def __repr__(self) -> str:
		string = "ColorBin({}, {}, '{}')".format(self.lower, self.upper, self.color)
		return string


class Palette:
	"""
		Parameters
		----------
		*args:
			divisions: List[Number]
			colors: List[str]
			lower: Tuple[Number, str]
			upper: Tuple[Number, str]
			missing: str
		**kwargs:
		* 'divisions'
		* 'colors'
		* 'lower'
		* 'upper'
		* 'missing'
	"""
	def __init__(self, *args, **kwargs):
		if args:
			divisions, colors, lower, upper, missing = args
		else:
			divisions = kwargs['divisions']
			colors = kwargs['colors']
			lower = kwargs['lower']
			upper = kwargs['upper']
			missing = kwargs['missing']

		self.bins: List[ColorBin] = [ColorBin(a, b, c) for a, b, c in zip(divisions[:-1], divisions[1:], colors)]
		self.lower: ColorPair = ColorPair(*lower)
		self.upper: ColorPair = ColorPair(*upper)
		self.missing: str = missing

	def __call__(self, value):
		return self.getColor(value)

	def getColor(self, value: float) -> str:
		value = float(value)

		if math.isnan(value):
			value_color = self.missing
		elif value < self.lower.value:
			value_color = self.lower.color
		elif value >= self.upper.value:
			value_color = self.upper.color
		else:
			for cbin in self.bins:
				if value in cbin:
					value_color = cbin.color
					break
			else:
				value_color = self.upper.color
		return value_color

	def toLegend(self) -> List[mpatches.Patch]:
		"""
			Converts the colormap into a matplotlib legend.
		"""
		max_length = len(str(int(self.upper.value)))

		_legend = [(self.lower.color, "Below {:.2f}".format(self.lower.value))]
		for color_bin in self.bins:
			string = "{0:>{2}.2f} - {1:>{2}.2f}".format(color_bin.lower, color_bin.upper, max_length)
			_legend.append((color_bin.color, string))
		_legend.append((self.upper.color, "Above {:.2f}".format(self.upper.value)))
		_legend.append((self.missing, "Missing data"))

		patches = [mpatches.Patch(color = c, label = l) for c, l in _legend]

		return patches

	def summary(self) -> None:
		print("Palette:")
		print("\tMissing Value: '{}'".format(self.missing))
		print("\tLower Limit: ", self.lower)
		print("\tUpper Limit: ", self.upper)
		print("\tColor Bins: ")
		for c in sorted(self.bins, key = lambda s: s.lower):
			print("\t\t", c)


class ColorMapGenerator:
	"""
		Usage
		-----
		colormap = ColorMap('percent')
		color = colormap(region, value)

		Colormap reference: https://matplotlib.org/examples/color/colormaps_reference.html

		Parameters
		----------
		values: Number, list<Number>, str
			Number: Used as the maximum with a minimum of 0.0
			list,Number>: the maximum and minimum will be used as the bounds for the colormap.
		breakpoint: float; default 0.0
			Used when generating a divergent colorscheme.

		Keyword Arguments
		-----------------

	"""

	def __init__(self, values: Union[str, Number, List[Number]], k: int = 6, breakpoint: Optional[Number] = None,
				 **kwargs):

		default_configuration: Dict[str, str] = {
			'missing_color': kwargs.get('missing_color', '#bdbdbd'),  # grey
			'colorscheme':   'Blues',
			'k':             k
		}

		values = self._getPredefinedValues(values)

		self.palette = self.generateLinearPalette(values, **default_configuration)

	@staticmethod
	def _getPredefinedValues(values: Union[str, List[Number]]) -> List[Number]:
		"""Returns a list of predefined values if none were given.
			Parameters
			----------
			values: list<Number> or {'percent'}
		"""

		defined_values = {
			'percent': list(range(0, 101, 10))
		}
		if isinstance(values, str):
			result = defined_values[values]
		elif isinstance(values, (int, float)):
			result = (0, values)
		else:
			result = values

		return sorted(result)

	@staticmethod
	def _generateQuantiles(values: List[Number], k: int = 6) -> List[Number]:
		"""
			Generates a list of quantile breakpoints.
		Parameters
		----------
		values: The values to use when generating quantiles. The minimum and maximum values are used as the bounds and
			the interior will be divided into 'k' bins.
		k: int; default 6
			The number of bins to generate.

		Returns
		-------

		"""
		minimum = min(values)
		maximum = max(values)

		difference = maximum - minimum

		result = [minimum + difference * index for index in range(0, k)]

		return result

	def generateLinearPalette(self, values: Iterable, k: int, colorscheme: str, **kwargs) -> Dict:
		minimum = min(values)
		maximum = max(values)
		width = (maximum - minimum) / k

		divisions = [width * i for i in range(k + 1)]

		colors = seaborn.mpl_palette(colorscheme, k + 2)
		colors = [self.rgbToHex(c) for c in colors]
		lower_default_color, *colors, upper_default_color = colors
		colormap_bins = list()

		for l, u, c in zip(divisions[:-1], divisions[1:], colors):
			binrange = ColorBin(l, u, c)
			colormap_bins.append(binrange)


		linear_palette = {
			'missing':  kwargs.get('missing_color', '#bdbdbd'),
			'lower': (minimum, lower_default_color),
			'upper': (maximum, upper_default_color),
			'divisions': divisions,
			'colors': colors
		}

		return linear_palette

	@staticmethod
	def rgbToHex(rgb: Tuple[float, float, float]) -> str:
		if isinstance(rgb, str):
			color = rgb
		else:
			color = "#{:>02X}{:>02X}{:>02X}".format(
				int(rgb[0] * 255),
				int(rgb[1] * 255),
				int(rgb[2] * 255)
			)
		return color

	def generateDivergentColormap(self, values: List[Number], breakpoint: Number):
		configuration: Dict[str, Optional[str]] = {
			'aboveBreakpoint':          'Blues',
			'belowBreakpoint':          'Reds',
			'atBreakpoint':             '#FFFFFF',
			'numAboveBreakpointColors': None,
			'numBelowBreakpointColors': None
		}
		breakpoint_color = configuration['atBreakpoint']
		above_values = [i for i in values if i > breakpoint]

		below_values = [breakpoint - i for i in above_values]

		above_breakpoint = seaborn.mpl_palette(configuration['aboveBreakpoint'], len(above_values))
		below_breakpoint = seaborn.mpl_palette(configuration['belowBreakpoint'], len(below_values))

		combined_values = sorted(below_values[1:]) + [breakpoint] + above_values

		combined_palette = below_breakpoint[::-1] + above_breakpoint
		# print(combined_palette)
		palette = [(v, self.rgbToHex(c)) for v, c in zip(combined_values, combined_palette)]

		print(combined_values)

		return palette


def generateColormap(*args, **kwargs) -> Palette:
	color_map_generator = ColorMapGenerator(*args, **kwargs)
	p = color_map_generator.palette

	return Palette(**p)


if __name__ == "__main__":
	palette = generateColormap((0, 60000))
	palette.summary()
