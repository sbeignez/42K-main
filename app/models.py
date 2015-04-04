import hashlib

from allauth.socialaccount.models import SocialAccount
from django.conf.global_settings import MEDIA_ROOT
from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize
# from geoposition.fields import GeopositionField
from payments.models import BasePayment


class AppUser(models.Model):
    ROLES = (
        ('admin', 'Admin'),
        ('photographer', 'Photographer'),
        ('runner', 'Runner'),
        ('tagger', 'Tagger'),
    )
    user = models.OneToOneField(User, related_name='app')
    role = models.CharField(max_length=15, choices=ROLES, default='runner')

    @property
    def facebooktoken(self):
        return self.user.socialaccount_set.first(
        ).socialtoken_set.first().token

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)

        return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())

    def __unicode__(self):
        return self.user.username

User.app = property(lambda u: AppUser.objects.get_or_create(user=u)[0])


class RaceEvent(models.Model):
    STATUSES = (
        ('submitted', 'submitted'),
        ('validated', 'validated'),
        ('deleted', 'deleted'),
    )
    name = models.CharField(max_length=50)
    date = models.DateTimeField()
    url = models.URLField()
    city = models.CharField(max_length=30)
    country = CountryField()
    bib_format = models.CharField(max_length=20)
    submitted_by = models.ForeignKey(User, related_name='%(class)s_submitted_by')
    validated_by = models.ForeignKey(User, related_name='%(class)s_validated_by')
    status = models.CharField(max_length=10, choices=STATUSES)

    def __unicode__(self):
        return self.name


class Photo(models.Model):
    file = models.ImageField(upload_to=MEDIA_ROOT, null=True, blank=True)
    thumb = ImageSpecField(source='file', processors=[SmartResize(256, 256)])
    # date = models.DateTimeField() upload date
    # date (photo date)
    # exif data
    race = models.ForeignKey(RaceEvent, related_name='%(class)s_race', default=None)
    # location = GeopositionField(default='0.0,0.0')
    # uploaded_by = models.ForeignKey(User, related_name='%(class)s_uploaded_by')

    def __unicode__(self):
        return self.file.path


class Payment(BasePayment):

    def get_failure_url(self):
        return "/orders"

    def get_success_url(self):
        return "/orders"

    def get_purchased_items(self):
        order = Order.objects.get(payment=self)
        items = OrderItem.objects.filter(order=order)
        for item in items:
            yield item


class Order(models.Model):
    user = models.ForeignKey(User, related_name='%(class)s_user')
    payment = models.ForeignKey(Payment, related_name='%(class)s_payment')
    items = models.ManyToManyField(Photo, through='OrderItem')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='%(class)s_order')
    photo = models.ForeignKey(Photo, related_name='%(class)s_photo')
    name = models.CharField(max_length=50, default='')
    sku = models.CharField(max_length=4, default='')
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=25.0)
    currency = models.CharField(max_length=3, default='USD')


class Tag(models.Model):
    photo = models.ForeignKey(Photo, related_name='%(class)s_photo')
    tagged_by = models.ForeignKey(User, related_name='%(class)s_tagged_by')
    bib = models.CharField(max_length=10)
    date = models.DateTimeField()
    # tag_date

    def __unicode__(self):
        return self.date + " " + self.bib
