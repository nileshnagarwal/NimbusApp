# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-08-09 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0015_auto_20190809_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiry',
            name='con_loading_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]