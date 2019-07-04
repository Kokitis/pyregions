import pandas

from pathlib import Path
from typing import Union, List, Tuple, Optional
from infotools.numbertools import to_number
ColumnsType = List[Union[str,int,float]]

def get_numeric_columns(columns: ColumnsType) -> ColumnsType:
	""" Returns a list of columns which refer to points in time."""
	numeric_columns = list()
	for col in columns:
		try:
			num = to_number(col, None)
			if num is not None: # may be 0
				numeric_columns.append(col)
		except ValueError:
			continue
	return numeric_columns


def _get_delimiter(path: Union[str,Path]) -> Optional[str]:
	""" Infers the correct delimiter to use when parsing the given csv/tsv file.
		Returns `None` if the path does not refer to a delimited file.
	"""
	path = Path(path)
	if path.suffix in {'.xlsx', '.xls'}:
		separator = None
	elif path.suffix in {'.tsv', '.tab'}:
		separator = '\t'
	else:
		separator = ','

	return separator


def load_table(path: Union[str, Path]) -> pandas.DataFrame:
	path = Path(path)
	sep = _get_delimiter(path)
	if sep:
		_table = pandas.read_table(path, sep = sep)
	else:
		_table = pandas.read_excel(path)

	return _table

def get_table(path:Union[str,Path])->Tuple[pandas.DataFrame, ColumnsType]:
	""" Loads a table and retrieves a list of the numeric columns."""
	table = load_table(path)
	ncols = get_numeric_columns(table.columns)
	return table, ncols

def save_table(table: pandas.DataFrame, path: Path) -> Path:
	path = Path(path)

	sep = _get_delimiter(path)
	if sep == '.xlsx':
		table.to_excel(str(path), index = False)
	else:
		table.to_csv(str(path), sep = sep, index = False)

	return path


