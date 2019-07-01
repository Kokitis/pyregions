"""
Implements a method of identifying a specific region based on name/country code and returns the iso-3 formatted code
for that region.
"""
from typing import Dict, Optional
from pathlib import Path
import pandas
import yaml
from fuzzywuzzy import process

DATA_FOLDER: Path = Path(__file__).parent / "data"
namespace_folder = DATA_FOLDER / "namespaces"
def _load_region_aliases()->pandas.DataFrame:
	alias_filename = DATA_FOLDER / "region_aliases.tsv"
	df = pandas.read_csv(alias_filename, sep = '\t')
	df = df.set_index('regionCode')
	df['regionName'] = df['regionName'].str.lower()
	return df

def _load_namespace(filename: Path) -> pandas.DataFrame:
	"""
		Loads a file from the `namespaces` folder. Should ba a yaml file.
	Parameters
	----------
	filename: Path

	Returns
	-------
	pandas.DataFrame
		- Columns-> `regionCode`, `regionName`
		- Index-> `standardCode`
	"""
	data = yaml.load(filename.read_text())
	namespace = data['regionMap']
	df = pandas.DataFrame.from_dict(namespace, orient = 'index')
	df.index.name = 'standardCode'
	df['namespace'] = data['name']
	return df


def _load_namespaces() -> pandas.DataFrame:
	dfs = list()
	for fn in namespace_folder.iterdir():
		if fn.suffix == '.yaml':
			dfs.append(_load_namespace(fn))
	return pandas.concat(dfs)


def identify(string: str, namespace: Optional[str] = None) -> Dict[str, str]:
	"""
		Identifies a region and returns the common name and iso-3 formatted region code.
	Parameters
	----------
	string:str
	namespace:Optional[str]
		Restricts the code search to the supplied namespace.

	Returns
	-------
	Tuple[str,str]
	- common name
	- region code
	"""
	string = string.lower()
	namespaces = _load_namespaces()
	if namespace:
		regions = namespaces[namespaces['namespace'] == namespace]
	else:
		regions = namespaces
	regions['regionName'] = regions['regionName'].str.lower()
	regions['regionCode'] = regions['regionCode'].str.lower()
	# Check if the given string is a valid code.
	if string in regions['regionCode'].tolist():
		region_code = regions.index[regions['regionCode'].tolist().index(string)]
	elif string in regions['regionName'].tolist():
		region_code =  regions.index[regions['regionName'].tolist().index(string)]
	else:
		region_code = search_aliases(string)
	if region_code:
		result = {
			'regionName': regions.loc[region_code].iloc[0]['regionName'],
			'regionCode': region_code.upper()
		}
	else:
		result = None
	return result


def search_aliases(string: str) -> Optional[str]:
	string = string.lower() # To avoid differences due to capitalization.
	region_aliases = _load_region_aliases()
	candidate, score, code = process.extractOne(string, region_aliases['regionName'])
	if score > 95:
		return code
	else:
		return None


if __name__ == "__main__":
	result = identify('united kingdom')

	print(result)
