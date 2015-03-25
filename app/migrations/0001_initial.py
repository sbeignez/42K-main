# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_countries.fields


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
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=50)),
                ('sku', models.CharField(default=b'', max_length=4)),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('price', models.DecimalField(default=25.0, max_digits=5, decimal_places=2)),
                ('currency', models.CharField(default=b'USD', max_length=3)),
                ('order', models.ForeignKey(related_name='orderitem_order', to='app.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('variant', models.CharField(max_length=255)),
                ('status', models.CharField(default='waiting', max_length=10, choices=[('waiting', 'Waiting for confirmation'), ('preauth', 'Pre-authorized'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected'), ('refunded', 'Refunded'), ('error', 'Error'), ('input', 'Input')])),
                ('fraud_status', models.CharField(default='unknown', max_length=10, verbose_name='fraud check', choices=[('unknown', 'Unknown'), ('accept', 'Passed'), ('reject', 'Rejected'), ('review', 'Review')])),
                ('fraud_message', models.TextField(default='', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('transaction_id', models.CharField(max_length=255, blank=True)),
                ('currency', models.CharField(max_length=10)),
                ('total', models.DecimalField(default='0.0', max_digits=9, decimal_places=2)),
                ('delivery', models.DecimalField(default='0.0', max_digits=9, decimal_places=2)),
                ('tax', models.DecimalField(default='0.0', max_digits=9, decimal_places=2)),
                ('description', models.TextField(default='', blank=True)),
                ('billing_first_name', models.CharField(max_length=256, blank=True)),
                ('billing_last_name', models.CharField(max_length=256, blank=True)),
                ('billing_address_1', models.CharField(max_length=256, blank=True)),
                ('billing_address_2', models.CharField(max_length=256, blank=True)),
                ('billing_city', models.CharField(max_length=256, blank=True)),
                ('billing_postcode', models.CharField(max_length=256, blank=True)),
                ('billing_country_code', models.CharField(max_length=2, blank=True)),
                ('billing_country_area', models.CharField(max_length=256, blank=True)),
                ('billing_email', models.EmailField(max_length=75, blank=True)),
                ('customer_ip_address', models.IPAddressField(blank=True)),
                ('extra_data', models.TextField(default='', blank=True)),
                ('message', models.TextField(default='', blank=True)),
                ('token', models.CharField(default='', max_length=36, blank=True)),
                ('captured_amount', models.DecimalField(default='0.0', max_digits=9, decimal_places=2)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.ImageField(upload_to=b'')),
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
                ('city', models.CharField(max_length=30)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('bib_format', models.CharField(max_length=20)),
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
            field=models.ForeignKey(related_name='photo_race', default=None, to='app.RaceEvent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='photo',
            field=models.ForeignKey(related_name='orderitem_photo', to='app.Photo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='app.Photo', through='app.OrderItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(related_name='order_payment', to='app.Payment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(related_name='order_user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
