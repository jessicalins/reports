from django.views.generic import ListView
from reportsapp.models import Device
from reportsapp.forms import PopularDevicesForm, FilterDevicesForm
from django.forms.models import model_to_dict
from django.shortcuts import render
from datetime import datetime, timedelta


class PopularDevicesView(ListView):
	def get_ten_most_popular_devices(self, dt):
		"""
		Return sorted list of 10 most popular devices
		"""
		all_devices = Device.objects.all()
		return sorted(all_devices,
		              key=lambda x: x.popularity(dt),
		              reverse=True)[:10]

	def create_devices_qs(self, dt):
		"""
		Returns list of popular devices
		"""
		popular_devices_qs = self.get_ten_most_popular_devices(dt)
		popular_devices = []
		for de in popular_devices_qs:
			device_dict = model_to_dict(de)
			device_dict['popularity'] = de.popularity(dt)
			device_dict['occurrences_weekly_changed'] = \
				de.occurrences_weekly_changed(dt)
			popular_devices.append(device_dict)
		return popular_devices

	def get(self, request, *args, **kwargs):
		form = PopularDevicesForm()
		current_date = datetime.now().date()
		popular_devices = self.create_devices_qs(current_date)
		return render(request,
		              'popular_devices.html',
		              {'form': form,
		               'popular_devices': popular_devices})

	def post(self, request, *args, **kwargs):
		form = PopularDevicesForm(request.POST)
		if form.is_valid():
			dt = form.cleaned_data.get('device_date', '')
			return render(request,
			              'popular_devices.html',
			              {'popular_devices': self.create_devices_qs(dt),
			               'form': form})
		return render(request, 'popular_devices.html')


class FilterDevicesView(ListView):
	def get_devices_count(self, d_type, status, dt):
		"""
		Returns total count of devices for a specific day
		"""
		return Device.objects.filter(device_type=d_type,
		                             occurrences__status=status,
		                             occurrences__timestamp__date=dt).count()

	def create_devices_list(self, d_type, status, selected_date):
		"""
		Returns filtered list of devices
		"""
		devices = []
		last_30_days = [selected_date - timedelta(days=x)
		                for x in range(0, 30)]

		for day in last_30_days:
			devices_info = {}
			devices_info['date'] = day.strftime('%d-%m-%Y')
			devices_info['count'] = self.get_devices_count(d_type, status, day)
			devices.append(devices_info)

		return devices

	def get(self, request, *args, **kwargs):
		form = FilterDevicesForm()
		devices_filtered_list = self.create_devices_list('sensor',
		                                                 'online',
		                                                 datetime.today())
		return render(request,
		              'devices_filtered_list.html',
		              {'form': form,
		               'devices_filtered_list': devices_filtered_list})

	def post(self, request, *args, **kwargs):
		form = FilterDevicesForm(request.POST)

		if form.is_valid():
			device_date = form.cleaned_data.get('device_date', '')
			device_type = form.cleaned_data.get('device_type', '')
			status = form.cleaned_data.get('status', '')

			return render(request,
			              'devices_filtered_list.html',
			              {'devices_filtered_list':
				              self.create_devices_list(
					              device_type, status, device_date),
			              'form': form})
		return render(request, 'devices_filtered_list.html')
