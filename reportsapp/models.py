from django.db import models
from datetime import timedelta


class Device(models.Model):
    device_ref = models.CharField(max_length=100, primary_key=True)
    device_type = models.CharField(max_length=200)

    def popularity(self, dt):
        return self.occurrences.filter(timestamp__date=dt).count()

    def occurrences_weekly_changed(self, dt):
        date_one_week_before = dt - timedelta(days=7)
        current_popularity = self.popularity(dt)
        old_popularity = self.popularity(date_one_week_before)

        if old_popularity == 0:
            # avoid division by zero
            return 0

        if current_popularity > old_popularity:
            # the device popularity increased
            return round(
                ((current_popularity - old_popularity) / old_popularity)
                * 100)
        # the device popularity decreased - so it is a negative number
        return -round(
            ((old_popularity - current_popularity) / old_popularity)
            * 100)


class Occurrence(models.Model):
    device = models.ForeignKey(Device, related_name='occurrences')
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=100)

    class Meta:
        # Ensures that for a specific device the timestamp is unique
        unique_together = ('device', 'timestamp',)
