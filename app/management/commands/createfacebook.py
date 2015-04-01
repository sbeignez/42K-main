from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not SocialApp.objects.filter(provider="facebook").exists():

            if settings.ENV == "test":
                app = SocialApp.objects.create(provider='facebook', name='Facebook',
                                               client_id='1586347994945475',
                                               secret='9f7ba3a75cd94cb947ab9f56cbb00068')
            else:
                app = SocialApp.objects.create(provider='facebook', name='Facebook',
                                               client_id='1582734425306832',
                                               secret='3de82319a1b1c2f37a23a7686935aa1e')

            app.sites.add(Site.objects.get_current())