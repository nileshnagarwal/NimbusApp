# Generated by Django 2.2.5 on 2019-11-14 17:29

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0013_auto_20191007_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='address',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
