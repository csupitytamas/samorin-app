from rest_framework import serializers
from .models import Pole, Wings, Warehouse

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

class PoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pole
        fields = '__all__'

class WingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wings
        fields = '__all__'