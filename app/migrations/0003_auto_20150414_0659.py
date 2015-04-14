# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150411_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='raceevent',
            name='distance',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='raceevent',
            name='name_vo',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='raceevent',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
