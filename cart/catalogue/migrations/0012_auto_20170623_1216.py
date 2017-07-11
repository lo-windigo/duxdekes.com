# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-23 19:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_auto_20140827_1705'),
        ('offer', '0003_auto_20161120_1707'),
        ('wishlists', '0002_auto_20160111_1108'),
        ('promotions', '0002_auto_20150604_1450'),
        ('partner', '0004_auto_20160107_1755'),
        ('order', '0005_update_email_length'),
        ('reviews', '0003_auto_20160802_1358'),
        ('basket', '0007_slugfield_noop'),
        ('customer', '0003_update_email_length'),
        ('catalogue', '0011_auto_20170613_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstructionsProduct',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='catalogue.Product')),
                ('sku', models.CharField(max_length=64)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('price_with_blank', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('alone_stock', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alone', to='partner.StockRecord')),
                ('blank', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paired_blank', to='catalogue.Product')),
                ('with_blank_stock', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='with_blank', to='partner.StockRecord')),
            ],
            options={
                'ordering': ['-date_created'],
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'abstract': False,
            },
            bases=('catalogue.product',),
        ),
        migrations.RemoveField(
            model_name='instructionswithblankproduct',
            name='blank',
        ),
        migrations.RemoveField(
            model_name='instructionswithblankproduct',
            name='product_ptr',
        ),
        migrations.DeleteModel(
            name='InstructionsWithBlankProduct',
        ),
    ]