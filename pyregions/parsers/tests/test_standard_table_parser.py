from pathlib import Path
import unittest
import pandas


from pyregions.parsers.parse_table import load_standard_table, StandardTable

class TestParser(unittest.TestCase):
	def setUp(self):
		self.filename:Path = Path(__file__).with_name('standard_table.tsv')
		self.truth_table = StandardTable.from_yaml(self.filename)

	def test_load_sandard_table(self):
		test_table = load_standard_table(self.filename)




if __name__ == "__main__":
	unittest.main()