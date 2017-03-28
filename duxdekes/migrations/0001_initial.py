# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-16 18:23
from __future__ import unicode_literals
from django.db import migrations
from django.apps import apps as global_apps
from duxdekes.util import dataimport


def import_data(x,y):
    # Just run it
    dataimport.import_data()

class Migration(migrations.Migration):

    atomic = False

    dependencies = [
    ]

    operations = [
        migrations.RunPython(import_data, migrations.RunPython.noop)
    ]
