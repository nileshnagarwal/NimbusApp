# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-08-20 12:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0010_auto_20190615_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicletype',
            name='vehicle',
            field=models.CharField(max_length=30),
        ),
    ]
