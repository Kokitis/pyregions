import argparse
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class FormatParser(argparse.Namespace):
	# For convienience
	input: Path
	output: Path
	column: str
	namespace: Optional[str]
	fuzzy: int

	@classmethod
	def from_parser(cls, parser) -> 'FormatParser':

		output = Path(parser.output) if parser.output else None
		return cls(Path(parser.input), output, parser.column, parser.namespace, int(parser.fuzzy))


def define_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(prog = 'pyregions')

	subparsers = parser.add_subparsers(help = "subcommands")

	utility_parser = subparsers.add_parser('format', help = "Utilities for formatting tables.")
	utility_parser.add_argument(
		"-i", "--input",
		help = "The table to convert.",
		action = "store",
		dest = "input"
	)
	utility_parser.add_argument(
		"-o", "--output",
		help = "Name of the new table. defaults to `input`.edited.tsv",
		action = 'store',
		dest = 'output',
		default = None
	)

	utility_parser.add_argument(
		"-c", "--column",
		help = "The table column to convert to ISO-3 codes.",
		action = 'store',
		dest = 'column',
		default = 'countryCode'
	)
	utility_parser.add_argument(
		"-n", "--namespace",
		help = "The code namespace of the table column. Speeds up the code search.",
		action = "store",
		dest = "namespace",
		default = None
	)
	utility_parser.add_argument(
		"-f", "--fuzzy",
		help = "Indicates that a fuzzy search should be used if greater than 0. Only useful if the table column contains names.",
		action = 'store',
		dest = 'fuzzy',
		default = 0
	)

	return parser


def utility_workflow(parser: argparse.Namespace):
	from utilities import country_codes
	parser = FormatParser.from_parser(parser)
	print(parser)
	country_codes.convert_table_codes(parser.input, parser.output, parser.column, parser.namespace, parser.fuzzy)


if __name__ == "__main__":
	print("Main")
	commands = define_parser()
	args = commands.parse_args()
	print(args)
	utility_workflow(args)
