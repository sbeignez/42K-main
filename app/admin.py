from django.contrib import admin
from app.models import RaceEvent, UserProfile, Tag, Photo

admin.site.register(UserProfile)
admin.site.register(RaceEvent)
admin.site.register(Photo)
admin.site.register(Tag)