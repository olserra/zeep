# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('address', models.CharField(max_length=20, null=True, blank=True)),
            ],
            options={
                'db_table': 'house',
                'managed': True,
            },
        ),
    ]
