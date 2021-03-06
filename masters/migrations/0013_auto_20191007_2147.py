# Generated by Django 2.2.5 on 2019-10-07 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0012_auto_20190921_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='neighbors',
            field=models.ManyToManyField(blank=True, related_name='_district_neighbors_+', to='masters.District'),
        ),
        migrations.AddField(
            model_name='district',
            name='unique_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
