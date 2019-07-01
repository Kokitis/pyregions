from pathlib import Path
import pandas
import math
from bs4 import UnicodeDammit
from io import StringIO
from loguru import logger
DATA_FOLDER = Path(__file__).parent / "data"

def get_namespace_iso()->pandas.DataFrame:
	""" Provides an ISO namespace table."""
	filename = DATA_FOLDER / "country-codes.tsv"
	table = pandas.read_csv(filename, sep = '\t')

	table['regionType'] = [("country" if i == 'yes' else "territory") for i in table['is_independent'].values]

	table = table[["official_name_en", "ISO3166-1-Alpha-2", "ISO3166-1-Alpha-3", "M49", 'regionType']]

	table.columns = ['regionName', 'iso2', 'iso3', 'ison', 'regionType']

	table['ison'] = table['ison'].apply(lambda s: f"{int(s):>03d}" if not math.isnan(s) else math.nan)

	return table

def get_namespace_usps()->pandas.DataFrame:
	filename = DATA_FOLDER / "usps_codes.tsv"
	table = pandas.read_csv(filename, sep = '\t')
	return table


