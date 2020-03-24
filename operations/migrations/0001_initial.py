# Generated by Django 2.2.5 on 2020-03-24 20:03

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('masters', '0020_client_clientaddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='LorryReceiptNo',
            fields=[
                ('lr_no', models.IntegerField(primary_key=True, serialize=False)),
                ('verification_no', models.CharField(blank=True, max_length=6)),
                ('vehicle_no', models.CharField(blank=True, max_length=12, null=True)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='masters.Client')),
            ],
        ),
        migrations.CreateModel(
            name='LorryReceipt',
            fields=[
                ('lr_no_id', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='operations.LorryReceiptNo')),
                ('date', models.DateField(default=datetime.date.today)),
                ('dispatch_from', models.CharField(max_length=255)),
                ('ship_to', models.CharField(max_length=255)),
                ('consignor_manual', models.CharField(blank=True, max_length=255, null=True)),
                ('consignee_manual', models.CharField(blank=True, max_length=255, null=True)),
                ('invoice_no', models.CharField(blank=True, max_length=255, null=True)),
                ('invoice_date', models.CharField(blank=True, max_length=255, null=True)),
                ('dc_no', models.CharField(blank=True, max_length=255, null=True)),
                ('dc_date', models.CharField(blank=True, max_length=255, null=True)),
                ('boe_no', models.CharField(blank=True, max_length=255, null=True)),
                ('boe_date', models.CharField(blank=True, max_length=255, null=True)),
                ('value', models.CharField(max_length=255)),
                ('ewaybill_no', models.CharField(max_length=255)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
                ('size', models.CharField(blank=True, max_length=255, null=True)),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('consignee_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lr_consignee', to='masters.ClientAddress')),
                ('consignor_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lr_consignor', to='masters.ClientAddress')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('packing_type', models.CharField(blank=True, max_length=255, null=True)),
                ('no_of_pkg', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('lr_no_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='item', to='operations.LorryReceipt')),
            ],
        ),
    ]
