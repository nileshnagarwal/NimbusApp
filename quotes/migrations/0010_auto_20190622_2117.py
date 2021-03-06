# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-06-22 15:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0009_auto_20190521_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='supplierquote',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplierquote',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='supplierquote',
            name='vehicle_body_id',
            field=models.ManyToManyField(blank=True, to='masters.VehicleBody'),
        ),
    ]
