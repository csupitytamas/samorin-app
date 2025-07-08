from rest_framework import serializers
from .models import Event, Arena, PoleLocation, WingLocation
from warehouse.models import Pole, Wings

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class ArenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arena
        fields = '__all__'

class PoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pole
        fields = ['name_hu', 'name_en', 'color', 'length', 'picture']

class WingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wings
        fields = ['name_hu', 'name_en', 'color', 'picture']

class PoleLocationSerializer(serializers.ModelSerializer):
    pole = PoleSerializer(read_only=True)  #

    class Meta:
        model = PoleLocation
        fields = ['id', 'pole', 'quantity', 'warehouse', 'arena']

class WingLocationSerializer(serializers.ModelSerializer):
    wing = WingSerializer(read_only=True)  # nested serializer a kapcsolódó wing mezőhöz

    class Meta:
        model = WingLocation
        fields = ['id', 'wing', 'quantity', 'warehouse', 'arena']