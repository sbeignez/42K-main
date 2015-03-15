from django.contrib import admin
from app.models import RaceEvent, AppUser, Tag, Photo, Payment, Order, OrderItem

admin.site.register(AppUser)
admin.site.register(RaceEvent)
admin.site.register(Photo)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(Tag)
