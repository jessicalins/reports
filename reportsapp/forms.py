from django import forms

DEVICE_TYPE_CHOICES = (('sensor','sensor'), ('gateway','gateway'))
DEVICE_STATUS_CHOICES = (('online','online'), ('offline','offline'))

class PopularDevicesForm(forms.Form):
	"""
	Form that receives a date to filter the list of popular devices
	"""
	device_date = forms.DateField(required=True,
	                              widget=forms.SelectDateWidget())


class FilterDevicesForm(forms.Form):
	"""
	Form that receives a date, type and status to filter list of devices
	"""
	device_date = forms.DateField(required=True,
	                              widget=forms.SelectDateWidget())
	device_type = forms.ChoiceField(choices=DEVICE_TYPE_CHOICES)
	status = forms.ChoiceField(choices=DEVICE_STATUS_CHOICES)
