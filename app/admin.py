from django.contrib import admin
from app.models import RaceEvent, AppUser, Tag, Photo

admin.site.register(AppUser)
admin.site.register(RaceEvent)
admin.site.register(Photo)
admin.site.register(Tag)
