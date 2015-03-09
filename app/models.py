from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    # add roles

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    class Meta:
        db_table = 'user_profile'


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