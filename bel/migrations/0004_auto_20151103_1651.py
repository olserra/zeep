# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bel', '0003_house_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(default=0, srid=4326),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='house',
            name='rdx',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='house',
            name='rdy',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
