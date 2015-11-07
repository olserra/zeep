# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bel', '0002_auto_20151103_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='link',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
