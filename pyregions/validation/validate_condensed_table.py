""" Provides a validator for tables with timepoints as individual columns"""
import pandas
from pyregions.standard_table_definition import RequiredColumns
def validate_table(table: pandas.DataFrame, columns:RequiredColumns = None)->bool:
	if columns is None: columns = RequiredColumns()
	# Validate columns
	## Find missing columns
	missing_columns = columns.find_missing_columns(table.columns)

	## Check for timepoint columns
	timepoint_columns = columns.find_timepoint_columns(table.columns)

	## Check timepoint column for invalid datatypes
	for tcol in timepoint_columns:
		dtype = table[tcol].dtypes



