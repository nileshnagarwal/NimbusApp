# Generated by Django 2.2.5 on 2020-04-02 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lorryreceipt',
            name='consignee_gstin',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lorryreceipt',
            name='consignor_gstin',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
