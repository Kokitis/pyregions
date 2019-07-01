
# Input

## CSV
Note that a csv_table will need the report and agency information provided
separately.

Contains the following columns:
#todo add report and agency columns
- `reportName`
- `reportUrl`
- `reportDate`
- `agencyName`
- `agencyUrl`
- `regionName`
- `regionCode`
- `seriesName`
- `seriesCode`
- `seriesDescription`
- `seriesNotes`
- `seriesScale`
- `seriesUnits`
- `seriesTags`
- one column per timepont.

Example:

| regionCode | seriesCode | regionName    | seriesName | seriesDescription | seriesUnits | seriesScale | sereisNotes | 1980    | 1990    | 2000    | 2010    | 2016    | 2017    | 2018    |
|------------|------------|---------------|------------|-------------------|-------------|-------------|-------------|---------|---------|---------|---------|---------|---------|---------|
| CAN        | LP         | Canada        | Population | …                 | Persons     | Millions    | …           | 24.471  | 27.632  | 30.647  | 33.959  | 36.205  | 36.657  | 37.108  |
| MEX        | LP         | Mexico        | Population | …                 | Persons     | Millions    | …           | 69.361  | 87.065  | 100.896 | 114.256 | 122.273 | 123.518 | 124.738 |
| USA        | LP         | United States | Population | …                 | Persons     | Millions    | …           | 227.622 | 250.047 | 282.296 | 309.749 | 323.572 | 325.886 | 328.434 |

## Excel Worksheet

The excel workbook should contain three sheets: `data`, `report`, `agency`.

### `report` sheet:
Columns:
- `reportName`
- `reprtDate`
- `reportUrl`

### `agency` sheet:
Columns:
- `agencyName`
- `agencyUrl`

### `data` sheet:
Same as the csv file above.

## Long Table

Each row can only contain a single timepoint.

Required columns:
- `regionName`
- `regionCode`
- `seriesName`
- `seriesCode`
- `seriesDescription`
- `seriesNotes`
- `seriesScale`
- `seriesUnit`
- `timepoint`
- `value`
