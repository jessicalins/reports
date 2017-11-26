import os
from datetime import datetime
from django.test import TestCase
from reportsapp.tasks import report_processing
from reportsapp.models import Device, Occurrence

CURRENT_DIR = os.getcwd()
CSV_FILE = \
    '{}/reportsapp/tests/csv_test_files/test_report.csv'.format(CURRENT_DIR)
CSV_FILE_DIFF_HEADER = \
    '{}/reportsapp/tests/csv_test_files/test_report_csv_header_diff.csv'. \
        format(CURRENT_DIR)
CSV_FILE_WITH_WRONG_DATA = \
    '{}/reportsapp/tests/csv_test_files/test_report_with_wrong_data.csv'. \
        format(CURRENT_DIR)


class ReportProcessingTestCase(TestCase):
    """
    Test task to parse the report.csv file
    """

    def test_report_processing(self):
        # test with normal csv file
        report_processing(CSV_FILE)
        dt = datetime.strptime('01-05-17', '%d-%m-%y').date()
        self.assertEqual(Occurrence.objects.count(), 17)
        self.assertEqual(Device.objects.filter(device_type='sensor').count(), 8)
        self.assertEqual(Device.objects.filter(device_type='gateway').count(), 7)
        self.assertEqual(Occurrence.objects.filter(status='online').count(), 8)
        self.assertEqual(Occurrence.objects.filter(status='offline').count(), 9)
        self.assertEqual(
            Occurrence.objects.filter(timestamp__date=dt).count(), 4)

        # clear db
        Device.objects.all().delete()

        # test csv with different header order
        report_processing(CSV_FILE_DIFF_HEADER)
        self.assertEqual(Occurrence.objects.count(), 17)
        self.assertEqual(Device.objects.filter(device_type='sensor').count(), 8)
        self.assertEqual(Device.objects.filter(device_type='gateway').count(),
                         7)
        self.assertEqual(Occurrence.objects.filter(status='online').count(), 8)
        self.assertEqual(Occurrence.objects.filter(status='offline').count(), 9)
        self.assertEqual(
            Occurrence.objects.filter(timestamp__date=dt).count(), 4)

        # clear db
        Device.objects.all().delete()

        # test with missing csv header
        with self.assertRaises(Exception):
            report_processing(CSV_FILE_WITH_WRONG_DATA)
            # it shouldn't have created any data
            self.assertEqual(Device.objects.count(), 0)
            self.assertEqual(Occurrence.objects.count(), 0)
