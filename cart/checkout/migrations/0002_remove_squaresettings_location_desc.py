# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-22 23:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='squaresettings',
            name='location_desc',
        ),
    ]
