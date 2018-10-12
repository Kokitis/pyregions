# The following is the standard table layout supported by the database.

# Timeseries Table
A common table format where timepoints correspond to a specific column

- timepoints are represented as specific columns
- rows correspond to a single series of timepoints
- observations are indexed by row and column.

# Condensed

Columns:
- regionName
- regionCode
- seriesCode
- variable
  - seriesDescription
  - seriesNotes
  - seriesScale
  - seriesUnit
  - seriesTags
  - timepoint
- value
  - timepoint|value


# Standard Table

Columns:
- regionName
- regionCode
- seriesName
- seriesCode
- seriesDescription
- seriesNotes
- seriesScale
- seriesUnit
- seriesTags
- each timepoint occupies a separate column

Rows:
- Each row represents a unique series for each region.

