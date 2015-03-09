from django.contrib import admin
from app.models import RaceEvent, UserProfile

admin.site.register(UserProfile)
admin.site.register(RaceEvent)