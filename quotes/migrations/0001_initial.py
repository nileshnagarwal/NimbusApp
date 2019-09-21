# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-02-20 13:35
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('masters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('enquiry_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('Floated Enquiry', 'Floated Enquiry'), ('Unfloated Enquiry', 'Unfloated Enquiry'), ('Confirmed Order', 'Confirmed Order')], default='Unfloated Enquiry', max_length=20)),
                ('length', models.DecimalField(decimal_places=2, max_digits=5)),
                ('width', models.DecimalField(decimal_places=2, max_digits=5)),
                ('height', models.DecimalField(decimal_places=2, max_digits=5)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('load_type', models.CharField(choices=[('ODC', 'ODC'), ('Normal', 'Normal'), ('Part', 'Part'), ('Container', 'Container')], default='Normal', max_length=10)),
                ('comments', models.TextField(blank=True, null=True)),
                ('enquiry_no', models.CharField(blank=True, max_length=255, null=True)),
                ('loading_date', models.DateTimeField(default=datetime.date.today)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('extra_expenses', models.ManyToManyField(blank=True, to='masters.ExtraExpenses')),
                ('user', models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehicle_body', models.ManyToManyField(blank=True, to='masters.VehicleBody')),
                ('vehicle_type', models.ManyToManyField(blank=True, to='masters.VehicleType')),
            ],
        ),
        migrations.CreateModel(
            name='SupplierQuote',
            fields=[
                ('quote_id', models.AutoField(primary_key=True, serialize=False)),
                ('rate', models.PositiveIntegerField()),
                ('including_fine', models.BooleanField()),
                ('vehicle_avail', models.BooleanField()),
                ('enquiry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='quotes.Enquiry')),
                ('transporter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='masters.Transporter')),
                ('user', models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehicle_type', models.ManyToManyField(to='masters.VehicleType')),
            ],
        ),
    ]
