# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-07-06 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0012_confirmenquiry_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmenquiry',
            name='enquiry_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
