from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not SocialApp.objects.filter(provider="facebook").exists():
            app = SocialApp.objects.create(provider='facebook', name='Facebook', client_id='1582734425306832',
                                         secret='bc30440a1f440c296f1f60775883aac1')
            app.sites.add(Site.objects.get_current())