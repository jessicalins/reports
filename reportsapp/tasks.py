from __future__ import absolute_import, unicode_literals
import os
from celery import shared_task
from django.utils.dateparse import parse_datetime
from reports.settings import BASE_DIR
from reportsapp.models import Device, Occurrence

REPORT_CSV_PATH = os.path.join(BASE_DIR, 'reportsapp/report.csv')


@shared_task
def report_processing(csv_file=REPORT_CSV_PATH):
    with open(csv_file) as file:
        first_line = list(map(lambda n: n.strip(), file.readline().split(',')))

        try:
            timestamp_index = first_line.index('timestamp')
            id_index = first_line.index('id')
            type_index = first_line.index('type')
            status_index = first_line.index('status')
        except ValueError:
            raise Exception('timestamp, id, type, status should be defined in '
                            'the first line of the csv.')

        for line in file:
            fields = line.split(',')
            # creates a new device
            device, created = Device.objects.update_or_create(
                device_ref=fields[id_index].strip(),
                device_type=fields[type_index].strip()
            )
            # creates a new occurrence
            Occurrence.objects.update_or_create(
                device=device,
                timestamp=parse_datetime(fields[timestamp_index].strip()),
                status=fields[status_index].strip()
            )
