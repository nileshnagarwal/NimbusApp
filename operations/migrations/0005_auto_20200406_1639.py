# Generated by Django 2.2.5 on 2020-04-06 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0004_lorryreceipt_vehicle_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lorryreceipt',
            name='ewaybill_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]