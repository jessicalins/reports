from django.test import TestCase
from django.urls import reverse
from django.test import RequestFactory
from reportsapp.views import PopularDevicesView, FilterDevicesView
from reportsapp.factories import DeviceFactory
from reportsapp.tests.utils import create_dates_in_range, create_occurrences
from django.utils.dateparse import parse_datetime

class PopularDevicesViewTestCase(TestCase):
	def test_get(self):
		"""
		Test that list of popular devices is shown properly
		"""
		request_factory = RequestFactory()
		request = request_factory.get(reverse('popular_devices'))
		response = PopularDevicesView.as_view()(request)

		self.assertEqual(response.status_code, 200)

	def test_post(self):
		"""
		Test filter by date
		"""
		# Create the request
		data = {
			'device_date': '2017-01-01',
		}
		request_factory = RequestFactory()
		request = request_factory.post(reverse('popular_devices'), data)

		# Get the response
		response = PopularDevicesView.as_view()(request)
		self.assertEqual(response.status_code, 200)

	def test_ten_most_popular_devices(self):
		"""
		Test ten most popular devices function
		"""
		devices = DeviceFactory.create_batch(15)
		dates = create_dates_in_range(0, 2, '2017-05-01T00:{}:40Z')
		create_occurrences(devices[0], dates)

		dates = create_dates_in_range(0, 6, '2017-05-01T00:{}:40Z')
		create_occurrences(devices[1], dates)

		dates = create_dates_in_range(0, 10, '2017-05-01T00:{}:40Z')
		create_occurrences(devices[2], dates)

		p = PopularDevicesView()
		popular_devices_list = p.get_ten_most_popular_devices(
			parse_datetime('2017-05-01T00:10:40Z').date())

		self.assertEqual(devices[2].device_ref,
		                 popular_devices_list[0].device_ref)
		self.assertEqual(devices[1].device_ref,
		                 popular_devices_list[1].device_ref)
		self.assertEqual(devices[0].device_ref,
		                 popular_devices_list[2].device_ref)

class FilterDevicesViewTestCase(TestCase):
	def test_get(self):
		"""
		Test that list of popular devices is shown properly
		"""
		request_factory = RequestFactory()
		request = request_factory.get(reverse('filter_devices'))
		response = FilterDevicesView.as_view()(request)

		self.assertEqual(response.status_code, 200)

	def test_post(self):
		"""
		Test filter by date
		"""
		# Create the request
		data = {
			'device_date': '2017-01-01',
			'device_type': 'sensor',
			'status': 'online'
		}
		request_factory = RequestFactory()
		request = request_factory.post(reverse('filter_devices'), data)

		# Get the response
		response = FilterDevicesView.as_view()(request)
		self.assertEqual(response.status_code, 200)
