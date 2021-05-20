# Generated by Django 2.2.5 on 2021-05-20 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0008_auto_20200406_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lorryreceipt',
            name='consignee_manual',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='lorryreceipt',
            name='consignor_manual',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='lorryreceipt',
            name='lr_no_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='lr_details', serialize=False, to='operations.LorryReceiptNo'),
        ),
    ]
