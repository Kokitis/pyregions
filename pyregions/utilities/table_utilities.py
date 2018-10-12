import pandas

from pathlib import Path
from typing import Union, List, Iterable, Tuple
ColumnsType = List[Union[str,int]]

def get_numeric_columns(columns: ColumnsType) -> ColumnsType:
	numeric_columns = list()
	for col in columns:
		try:
			int(col)
			numeric_columns.append(col)
		except ValueError:
			continue
	return numeric_columns


def _get_delimiter(path: Path) -> str:
	if path.suffix in {'.xlsx', '.xls'}:
		separator = '.xlsx'
	elif path.suffix in {'.tsv', '.tab'}:
		separator = '\t'
	else:
		separator = ','

	return separator


def load_table(path: Union[str, Path]) -> pandas.DataFrame:
	path = Path(path)
	sep = _get_delimiter(path)
	if sep == '.xlsx':
		_table = pandas.read_excel(str(path))
	else:
		_table = pandas.read_table(str(path), sep = sep)
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


