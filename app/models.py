from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
from geoposition.fields import GeopositionField


class AppUser(models.Model):
    ROLES = (
        ('admin', 'Admin'),
        ('photographer', 'Photographer'),
        ('runner', 'Runner'),
        ('tagger', 'Tagger'),
    )
    user = models.OneToOneField(User, related_name='user')
    role = models.CharField(max_length=15, choices=ROLES, default='runner')

    def __unicode__(self):
        return self.user.username


class RaceEvent(models.Model):
    STATUSES = (
        ('submitted', 'submitted'),
        ('validated', 'validated'),
        ('deleted', 'deleted'),
    )
    name = models.CharField(max_length=50)
    date = models.DateTimeField()
    url = models.URLField()
    city = models.CharField(max_length=20)
    country = CountryField()
    bib_format = models.CharField(max_length=10)
    submitted_by = models.ForeignKey(User, related_name='%(class)s_submitted_by')
    validated_by = models.ForeignKey(User, related_name='%(class)s_validated_by')
    status = models.CharField(max_length=10, choices=STATUSES)

    def __unicode__(self):
        return self.name


class Photo(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(default='')
    date = models.DateTimeField()
    location = GeopositionField(default='0.0,0.0')
    uploaded_by = models.ForeignKey(User, related_name='%(class)s_uploaded_by')
    race = models.ForeignKey(RaceEvent, related_name='%(class)s_race')

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    photo = models.ForeignKey(Photo, related_name='%(class)s_photo')
    tagged_by = models.ForeignKey(User, related_name='%(class)s_tagged_by')
    bib = models.CharField(max_length=10)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.date + " " + self.bib