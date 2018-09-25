from pathlib import Path
import csv
from dataclasses import dataclass, asdict
from typing import Dict, Optional
from fuzzywuzzy import process
from pyregions.utilities import load_table, save_table

COUNTRY_CODE_FILENAME = Path(__file__).parent / "data" / "country-codes.csv"


@dataclass
class CountryCode:
	name: str
	iso2: str
	iso3: str
	m49: str  # https://unstats.un.org/unsd/methodology/m49/
	ison: int

def _get_separator():
	return None


def get_codes(key: str, namespace: str = None) -> Optional[Dict[str, str]]:
	"""
	Retrieves a code based on the given key. Searches for the first matching key in any field if namespace is not
	given.
	Parameters
	----------
	key: str
		The string to search for.
	namespace: {'iso2', 'iso3', 'ison', 'm49'}; default None

	Returns
	-------
	country_code: str
	"""

	if namespace: namespace = namespace.lower()

	for country in COUNTRY_CODES.values():
		if namespace:
			if key == country[namespace]:
				return country
		else:
			if key in country.values():
				return country


def convert_table_codes(input_filename: Path, output_filename: Path = None, column: str = 'countryCode',
		namespace: Optional[str] = None, fuzzy:int = 0) -> Path:
	"""
	Adds a 'regionCode' column to the given table containing iso-3 country codes.
	Parameters
	----------
	input_filename: Path
	output_filename: Path
	column: str, default 'countryCode
	namespace: {'iso2', 'iso3', 'm49'}; default None
	fuzzy: int; default 0
		The score to use when fuzzy matching when above 0. If 0, the regular code search is used instead.
	Returns
	-------
	path: Path
		Location of the output table.
	"""

	table = load_table(input_filename)

	if column not in table.columns:
		message = "'{}' is not a valid column. Expected one of {}".format(column, list(table.columns))
		raise ValueError(message)

	old_values = table[column].values

	if fuzzy:
		new_values = [fuzzy_search(i,fuzzy) for i in old_values]
	else:

		new_values = [get_codes(i, namespace) for i in old_values]

	new_values = [(v['iso3'] if v else v) for v in new_values]

	table['regionCode'] =  new_values

	if output_filename is None:
		output_filename = input_filename.with_suffix('.edited.tsv')
	elif output_filename.is_dir():
		output_filename = output_filename / input_filename.name

	opath = save_table(table, output_filename)
	return opath

def fuzzy_search(key: str, score = 95) -> Dict[str, str]:
	"""
		Attempts to find a country by name.
	Parameters
	----------
	key: str
		The name to search for.
	score: int; default 95
		The breakpoint to consider a key a match.

	Returns
	-------
	str
	the country code.
	"""
	best_match, ratio = process.extractOne(key, COUNTRY_CODES.keys())

	if best_match and ratio >= score:
		return COUNTRY_CODES[best_match]


def load_country_codes(filename: Path = COUNTRY_CODE_FILENAME) -> Dict[str, Dict[str, str]]:
	codes = dict()
	with filename.open('r') as code_file:
		reader = csv.DictReader(code_file, delimiter = '\t')

		for line in reader:
			name = line['name']

			iso2 = line['ISO3166-1-Alpha-2']
			iso3 = line['ISO3166-1-Alpha-3']
			m49 = line['M49']
			try:
				ison = int(m49)
			except ValueError:
				ison = None

			codes[name] = asdict(CountryCode(name, iso2, iso3, m49, ison))  # Use a dict so fuzzy search is easier.
	return codes


COUNTRY_CODES = load_country_codes()
if __name__ == "__main__":
	tests = ['US', 'Australia']

	for t in tests:
		print(get_codes(t))
