# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-02-20 13:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quotes', '0001_initial'),
        ('masters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='enquiry_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='quotes.Enquiry'),
        ),
    ]
