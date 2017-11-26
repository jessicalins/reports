import factory
from reportsapp.models import Device, Occurrence

TYPE_CHOICES = ['sensor', 'gateway']
STATUS_CHOICES = ['online', 'offline']


class DeviceFactory(factory.django.DjangoModelFactory):
    device_ref = factory.Faker('uuid4')
    device_type = factory.Iterator(TYPE_CHOICES)

    class Meta:
        model = Device


class OccurrenceFactory(factory.django.DjangoModelFactory):
    device = factory.SubFactory(DeviceFactory)
    timestamp = factory.Faker('date_time_this_year')
    status = factory.Iterator(STATUS_CHOICES)

    class Meta:
        model = Occurrence
