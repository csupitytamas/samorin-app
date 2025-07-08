from django.contrib import admin
from .models import Event, Arena, PoleLocation, WingLocation

admin.site.register(Event)
admin.site.register(Arena)
admin.site.register(PoleLocation)
admin.site.register(WingLocation)