# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields
import django_countries.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(default=b'runner', max_length=15, choices=[(b'admin', b'Admin'), (b'photographer', b'Photographer'), (b'runner', b'Runner'), (b'tagger', b'Tagger')])),
                ('user', models.OneToOneField(related_name='app', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(default=b'', upload_to=b'')),
                ('date', models.DateTimeField()),
                ('location', geoposition.fields.GeopositionField(default=b'0.0,0.0', max_length=42)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RaceEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('url', models.URLField()),
                ('city', models.CharField(max_length=20)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('bib_format', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=10, choices=[(b'submitted', b'submitted'), (b'validated', b'validated'), (b'deleted', b'deleted')])),
                ('submitted_by', models.ForeignKey(related_name='raceevent_submitted_by', to=settings.AUTH_USER_MODEL)),
                ('validated_by', models.ForeignKey(related_name='raceevent_validated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bib', models.CharField(max_length=10)),
                ('date', models.DateTimeField()),
                ('photo', models.ForeignKey(related_name='tag_photo', to='app.Photo')),
                ('tagged_by', models.ForeignKey(related_name='tag_tagged_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='photo',
            name='race',
            field=models.ForeignKey(related_name='photo_race', to='app.RaceEvent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='uploaded_by',
            field=models.ForeignKey(related_name='photo_uploaded_by', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
