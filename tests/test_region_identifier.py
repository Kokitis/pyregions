from pyregions.geotools.region_identifier import identify
import pytest

@pytest.mark.parametrize(
	"string",
	[
		'United Kingdom',
		"united kingdom",
		'United Kindom o Great Britain and Northern Ireland',
		'GBR', "GB"
	]
)

def test_identifier(string):
	expected_result = {
		'regionName': 'united kingdom',
		'regionCode': 'GBR'
	}
	result = identify(string)
	assert result == expected_result