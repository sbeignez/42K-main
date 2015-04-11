# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RaceUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('race', models.ForeignKey(related_name='raceuser_user', to='app.RaceEvent')),
                ('user', models.ForeignKey(related_name='raceuser_user', to='app.AppUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='order',
            old_name='items',
            new_name='photos',
        ),
        migrations.AddField(
            model_name='appuser',
            name='races',
            field=models.ManyToManyField(to='app.RaceEvent', through='app.RaceUser'),
            preserve_default=True,
        ),
    ]
