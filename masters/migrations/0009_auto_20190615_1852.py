# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-06-15 13:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0008_auto_20190615_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transporter',
            name='office_lat',
            field=models.DecimalField(decimal_places=20, default=0, max_digits=24),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transporter',
            name='office_lng',
            field=models.DecimalField(decimal_places=20, default=0, max_digits=24),
            preserve_default=False,
        ),
    ]
