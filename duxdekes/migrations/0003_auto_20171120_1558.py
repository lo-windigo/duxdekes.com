# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-20 23:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('duxdekes', '0002_auto_20171023_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sites.Site'),
        ),
    ]
