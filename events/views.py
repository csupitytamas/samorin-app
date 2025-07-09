from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event, Arena, PoleLocation, WingLocation
from .serializers import EventSerializer, ArenaSerializer, PoleLocationSerializer, WingLocationSerializer, \
    ArchivedEventDetailSerializer
from django.utils import timezone
from .models import ArchivedEvent, ArchivedArena, ArchivedPoleLocation, ArchivedWingLocation

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer

    @action(detail=True, methods=['get'])
    def full_details(self, request, pk=None):
        event = self.get_object()
        arenas = Arena.objects.filter(event=event)
        arenas_data = []
        for arena in arenas:
            pole_locations = PoleLocation.objects.filter(arena=arena)
            wing_locations = WingLocation.objects.filter(arena=arena)
            arenas_data.append({
                'arena': ArenaSerializer(arena).data,
                'poles': PoleLocationSerializer(pole_locations, many=True).data,
                'wings': WingLocationSerializer(wing_locations, many=True).data,
            })
        return Response({'arenas': arenas_data})

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        event = self.get_object()
        # Már archivált? Dupla archiválás ellenőrzése
        if event.is_archived:
            return Response({'detail': 'Already archived.'}, status=400)
        # 1. Archív event létrehozás
        archived_event = ArchivedEvent.objects.create(event=event, closed_at=timezone.now())
        # 2. Minden arena archiválása
        for arena in Arena.objects.filter(event=event):
            archived_arena = ArchivedArena.objects.create(
                archived_event=archived_event,
                name=arena.name
            )
            # 3. Minden pole location archiválása
            for ploc in PoleLocation.objects.filter(arena=arena):
                ArchivedPoleLocation.objects.create(
                    archived_arena=archived_arena,
                    pole_name=ploc.pole.name_en,
                    color=ploc.pole.color,
                    length=ploc.pole.length,
                    quantity=ploc.quantity
                )
                # 4. Pole warehouse növelése (visszaadás)
                ploc.pole.number += ploc.quantity
                ploc.pole.save()
            # 5. Minden wing location archiválása
            for wloc in WingLocation.objects.filter(arena=arena):
                ArchivedWingLocation.objects.create(
                    archived_arena=archived_arena,
                    wing_name=wloc.wing.name_en,
                    color=wloc.wing.color,
                    quantity=wloc.quantity
                )
                wloc.wing.number += wloc.quantity
                wloc.wing.save()
        # 6. Esemény archiválása
        event.is_archived = True
        event.is_active = False
        event.save()
        return Response({'detail': 'Event archived, all stock returned to warehouse.'})

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


class ArchivedEventDetailView(RetrieveAPIView):
    queryset = ArchivedEvent.objects.all()
    serializer_class = ArchivedEventDetailSerializer

class ArchivedEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArchivedEvent.objects.all()
    serializer_class = ArchivedEventDetailSerializer