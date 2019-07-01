from pyregions.dataio import datasets

def test_iso():
	table = datasets.get_namespace_iso()

	assert list(table.columns) == ['regionName', 'iso2', 'iso3', 'ison', 'regionType']

	# Make sure each column has the right datatype and no missing values (except ison)
	assert table['regionName'].tolist() == table['regionName'].apply(lambda s: str(s)).tolist()
	assert table['regionType'].tolist() == table['regionType'].apply(lambda s: str(s)).tolist()

	# The codes are optional, so nan values are allowed. make sure that the `ison` column is str, not float.
	values = table['ison'].dropna()
	assert values.tolist() == [str(i) for i in values.tolist()]
	# Make sure nan values were not accidently added
	assert 'nan' not in table['ison'].values

def test_get_usps():
	table = datasets.get_namespace_usps()

	# There should be a code for every region
	# Every field should have a value
	assert table['regionName'].tolist() == [str(i) for i in table['regionName'].tolist()]
	assert table['regionType'].tolist() == [str(i) for i in table['regionType'].tolist()]
	assert table['usps'].tolist() == [str(i) for i in table['usps'].tolist()]

	# Every code should be prefaced with 'USA-'
	assert [i.split('-')[0] for i in table['usps'].tolist()] == ['USA' for _ in range(len(table))]

	# Test a few codes
	assert 'USA-NY' in table['usps'].tolist()
	assert 'NY' not in table['usps'].tolist()
	assert 'USA-PR' in table['usps'].tolist()
	assert 'USA-DC' in table['usps'].tolist()



