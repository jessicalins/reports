from django.utils.dateparse import parse_datetime
from reportsapp.factories import OccurrenceFactory

def create_dates_in_range(n1, n2, timestamp_formatted):
	"""
	Returns list of dates with different times
	"""
	dates = []
	for i in range(n1, n2):
		dates.append(parse_datetime(timestamp_formatted.format(i)))
	return dates


def create_occurrences(device, dates):
	"""
	Create occurrences for a device from a list of dates
	"""
	occurrences = []
	for d in dates:
		# create occurrences for different times, but for the same date
		occurrences.append(
			OccurrenceFactory(device=device, timestamp=d))
	return occurrences