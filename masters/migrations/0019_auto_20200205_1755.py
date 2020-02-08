# Generated by Django 2.2.5 on 2020-02-05 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0018_loadtype_load_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loadtype',
            name='load_size',
            field=models.CharField(blank=True, choices=[('ODC', 'ODC'), ('FTL', 'FTL'), ('LTL', 'LTL')], max_length=20, null=True),
        ),
    ]
