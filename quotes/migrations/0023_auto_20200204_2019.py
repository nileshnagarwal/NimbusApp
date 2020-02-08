# Generated by Django 2.2.5 on 2020-02-04 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0022_remove_enquiry_load_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplierquote',
            name='freight',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='supplierquote',
            name='including_fine',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]