from rest_framework import serializers
from users.models import UserProfile
from .models import Event, Arena, PoleLocation, WingLocation, ArchivedEvent, ArchivedArena, ArchivedWingLocation, \
    ArchivedPoleLocation
from warehouse.models import Pole, Wings

class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
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
    pole = PoleSerializer(read_only=True)
    pole_id = serializers.PrimaryKeyRelatedField(
        queryset=Pole.objects.all(),
        source='pole',
        write_only=True
    )

    def create(self, validated_data):
        pole = validated_data['pole']
        quantity = validated_data['quantity']
        arena = validated_data.get('arena', None)

        if pole.number < quantity:
            raise serializers.ValidationError("Not enough poles in stock.")

        # Készlet csökkentése
        pole.number -= quantity
        pole.save()

        # Ha már létezik ilyen pole-arena páros, növeld a quantity-t!
        pole_location, created = PoleLocation.objects.get_or_create(
            pole=pole, arena=arena,
            defaults={'quantity': 0}
        )
        pole_location.quantity += quantity
        pole_location.save()

        return pole_location

    class Meta:
        model = PoleLocation
        fields = ['id', 'pole', 'pole_id', 'quantity', 'arena']
        unique_together = ('pole', 'arena')


class WingLocationSerializer(serializers.ModelSerializer):
    wing = WingSerializer(read_only=True)
    wing_id = serializers.PrimaryKeyRelatedField(
        queryset=Wings.objects.all(),
        source='wing',
        write_only=True
    )

    def create(self, validated_data):
        wing = validated_data['wing']
        quantity = validated_data['quantity']
        arena = validated_data.get('arena', None)

        if wing.number < quantity:
            raise serializers.ValidationError("Not enough wings in stock.")

        wing.number -= quantity
        wing.save()

        # Ha már létezik ilyen wing-arena páros, növeld a quantity-t!
        wing_location, created = WingLocation.objects.get_or_create(
            wing=wing, arena=arena,
            defaults={'quantity': 0}
        )
        wing_location.quantity += quantity
        wing_location.save()

        return wing_location

    class Meta:
        model = WingLocation
        fields = ['id', 'wing', 'wing_id', 'quantity', 'arena']
        unique_together = ('wing', 'arena')


class ArchivedPoleLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivedPoleLocation
        fields = ['pole_name', 'color', 'length', 'quantity']

class ArchivedWingLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivedWingLocation
        fields = ['wing_name', 'color', 'quantity']

class ArchivedArenaSerializer(serializers.ModelSerializer):
    poles = serializers.SerializerMethodField()
    wings = serializers.SerializerMethodField()

    class Meta:
        model = ArchivedArena
        fields = ['id', 'name', 'poles', 'wings']

    def get_poles(self, obj):
        poles = ArchivedPoleLocation.objects.filter(archived_arena=obj)
        return ArchivedPoleLocationSerializer(poles, many=True).data

    def get_wings(self, obj):
        wings = ArchivedWingLocation.objects.filter(archived_arena=obj)
        return ArchivedWingLocationSerializer(wings, many=True).data

class ArchivedEventDetailSerializer(serializers.ModelSerializer):
    arenas = serializers.SerializerMethodField()
    event_name = serializers.CharField(source='event.name', read_only=True)
    event_start = serializers.DateField(source='event.start_date', read_only=True)
    event_end = serializers.DateField(source='event.end_date', read_only=True)

    class Meta:
        model = ArchivedEvent
        fields = ['id', 'event_name', 'event_start', 'event_end', 'closed_at', 'arenas']

    def get_arenas(self, obj):
        arenas = ArchivedArena.objects.filter(archived_event=obj)
        return ArchivedArenaSerializer(arenas, many=True).data

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'email', 'role']

