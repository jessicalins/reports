# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-26 11:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reportsapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='occurrence',
            unique_together=set([('device', 'timestamp')]),
        ),
    ]