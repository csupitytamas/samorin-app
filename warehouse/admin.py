from django.contrib import admin
from .models import Warehouse, Pole, Wings

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Pole)
class PoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_hu', 'name_en', 'warehouse', 'color', 'number', 'length')

@admin.register(Wings)
class WingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_hu', 'name_en', 'warehouse', 'color', 'number')