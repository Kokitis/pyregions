import pandas

from pathlib import Path
from typing import Union


def _get_delimiter(path: Path) -> str:
	if path.suffix in {'.xlsx', '.xls'}:
		separator = 'xlsx'
	elif path.suffix in {'.tsv', 'tab'}:
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
		_table = pandas.read_table(sep = sep)
	return _table


def save_table(table: pandas.DataFrame, path: Path) -> Path:
	path = Path(path)

	sep = _get_delimiter(path)
	if sep == '.xlsx':
		table.to_excel(str(path))
	else:
		table.to_csv(str(path))

	return path
