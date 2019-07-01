import pytest
from pyregions import standard_definition

@pytest.fixture
def default_required_columns()->standard_definition.RequiredColumns:
	return standard_definition.RequiredColumns()

def test_required_columns_using_default_values(default_required_columns):
	default_columns = [
		'regionCode', 'regionName', 'seriesCode', 'seriesName', 'seriesNotes', 'seriesScale', 'seriesUnits', 'seriesDescription', 'seriesTags'
	]
	# Should Be []
	assert not default_required_columns.find_missing_columns(default_columns)

	default_columns_with_extra = default_columns + ['extraColumn1', 'extraColumn2']

	# Should be []
	assert not default_required_columns.find_missing_columns(default_columns_with_extra)

	with pytest.raises(ValueError):
		default_required_columns.find_missing_columns(default_columns[1:] + ['extra1', 'extra2'])

	# Now test if the optional 'tags' column throws an error if it is missing.
	assert not default_required_columns.find_missing_columns(default_columns[:-1] + ['extra1', 'extra2'])

def test_required_columns_using_custom_column_names(default_required_columns):
	default_required_columns.region_name_column = 'region'
	default_required_columns.note_column = 'notes'

	correct_columns = [
		'regionCode', 'region', 'seriesCode', 'seriesName', 'notes', 'seriesScale', 'seriesUnits', 'seriesDescription', 'seriesTags'
	]

	assert not default_required_columns.find_missing_columns(correct_columns)

	wrong_columns = [
		'regionCode', 'regionName', 'seriesCode', 'seriesName', 'seriesNotes', 'seriesScale', 'seriesUnits', 'seriesDescription', 'seriesTags'
	]

	with pytest.raises(ValueError):
		default_required_columns.find_missing_columns(wrong_columns)