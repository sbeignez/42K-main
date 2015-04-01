# custom_storages.py
from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

class StaticStorage(S3BotoStorage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME_STATIC
    location = settings.STATICFILES_LOCATION
    custom_domain = "%s/%s" % (settings.AWS_S3_DOMAIN, settings.AWS_STORAGE_BUCKET_NAME_STATIC)

class MediaStorage(S3BotoStorage):

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME_MEDIA
    location = settings.MEDIAFILES_LOCATION
    custom_domain = "%s/%s" % (settings.AWS_S3_DOMAIN, settings.AWS_STORAGE_BUCKET_NAME_MEDIA)

    def path(self, name):
        return self._normalize_name(name)

