# Generated by Django 2.2.5 on 2020-04-06 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0007_auto_20200406_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.CharField(default='WasNone', max_length=255),
            preserve_default=False,
        ),
    ]