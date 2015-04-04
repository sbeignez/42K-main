from cStringIO import StringIO

from PIL import Image

from app.models import RaceEvent, User
from django.core.files.base import ContentFile
from django.test import TestCase
from django.utils.timezone import now


class MainTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('user', None, 'pass')
        assert self.client.login(username='user', password='pass')

    def test_upload(self):
        # test get
        r = self.client.get('/photographer/')
        self.assertContains(r, 'Add files')

    def test_js_upload(self):
        race = RaceEvent.objects.create(
            date=now(), submitted_by=self.user, validated_by=self.user)
        img = StringIO()
        Image.new('RGB', (1, 1)).save(img, format='jpeg')
        r = self.client.post('/upload/', {
            'raceevent': race.pk, 'files[]': ContentFile(
                img.getvalue(), name='test.jpg')})
        self.assertContains(r, '{')
