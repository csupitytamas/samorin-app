from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event, Arena, PoleLocation, WingLocation
from .serializers import EventSerializer, ArenaSerializer, PoleLocationSerializer, WingLocationSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class ArenaViewSet(viewsets.ModelViewSet):
    queryset = Arena.objects.all()
    serializer_class = ArenaSerializer


class PoleLocationViewSet(viewsets.ModelViewSet):
    queryset = PoleLocation.objects.all()
    serializer_class = PoleLocationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['arena']


class WingLocationViewSet(viewsets.ModelViewSet):
    queryset = WingLocation.objects.all()
    serializer_class = WingLocationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['arena']