# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-05-12 08:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0005_auto_20190512_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplierquote',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='supplierquote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
