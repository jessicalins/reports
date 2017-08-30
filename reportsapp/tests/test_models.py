from django.test import TestCase
from django.utils.dateparse import parse_datetime
from reportsapp.factories import DeviceFactory, OccurrenceFactory
from reportsapp.tests.utils import create_dates_in_range, create_occurrences

class ModelsTestCase(TestCase):
	def test_device_popularity(self):
		"""
		Test if device's popularity is calculated correctly
		"""
		less_popular_device = DeviceFactory()
		dates = create_dates_in_range(10, 15, '2017-05-01T00:{}:40Z')
		create_occurrences(less_popular_device, dates)

		self.assertEqual(less_popular_device.popularity(dates[0].date()), 5)

	def test_occurrences_weekly_changed(self):
		"""
		Test if device's occurrences percentage change is calculated correctly
		"""
		current_date = parse_datetime('2017-05-08T00:20:40Z').date()
		device = DeviceFactory()

		# create 10 occurrences for the current date
		dates = create_dates_in_range(0, 10, '2017-05-08T00:{}:40Z')
		create_occurrences(device, dates)

		# create 5 occurrences for the last week
		dates_last_week = create_dates_in_range(
			0, 5, '2017-05-01T00:{}:40Z')
		create_occurrences(device, dates_last_week)

		# the popularity should increase 100%
		self.assertEqual(device.occurrences_weekly_changed(current_date), 100)

		# clean up occurrences
		device.occurrences.all().delete()

		# create 5 occurrences for the current date
		dates = create_dates_in_range(0, 5, '2017-05-08T00:{}:40Z')
		create_occurrences(device, dates)

		# create 10 occurrences for the last week
		dates_last_week = create_dates_in_range(
			0, 10, '2017-05-01T00:{}:40Z')
		create_occurrences(device, dates_last_week)

		# the popularity should increase 50%
		self.assertEqual(device.occurrences_weekly_changed(current_date), -50)
