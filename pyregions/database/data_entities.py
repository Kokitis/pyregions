from pytools.datatools import dataclass
from typing import Set, List
import datetime


@dataclass
class DataAgency:
	name: str
	url: str
	reports: List['DataRegion']


@dataclass
class DataReport:
	name: str
	agency: DataAgency
	url: str
	date: datetime.datetime
	series: List['DataSeries']


@dataclass
class DataRegion:
	code: str
	name: str
	type: str
	series: List['DataSeries']


@dataclass
class DataSeries:
	region: DataRegion
	report: DataReport
	code: str
	name: str
	description: str
	notes: str
	scale: 'DataScale'
	tags: List[str]


@dataclass
class DataScale:
	code: str
	unit: str
	multiplier: float


@dataclass
class DataTag:
	value: str
	series: List['DataSeries']

if __name__ == "__main__":
	pass
