# Generated by Django 2.2.5 on 2022-05-17 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0023_auto_20200204_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplierresponse',
            name='quote_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='quotes.SupplierQuote'),
        ),
    ]
