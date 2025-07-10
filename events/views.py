from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event, Arena, PoleLocation, WingLocation
from .serializers import EventSerializer, ArenaSerializer, PoleLocationSerializer, WingLocationSerializer, \
    ArchivedEventDetailSerializer
from django.utils import timezone
from .models import ArchivedEvent, ArchivedArena, ArchivedPoleLocation, ArchivedWingLocation
from .permissions import IsAdminOrReadOnly, IsCrewOrAdmin, IsChiefOrAdmin
from wishlist.serializers import WishlistSerializer
from wishlist.models import Wishlist

class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
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
        if event.is_archived:
            return Response({'detail': 'Already archived.'}, status=400)
        archived_event = ArchivedEvent.objects.create(event=event, closed_at=timezone.now())
        for arena in Arena.objects.filter(event=event):
            # IDE jön ez a sor!:
            archived_arena = ArchivedArena.objects.create(
                archived_event=archived_event,
                name=arena.name,
                original_arena_id=arena.id  # <-- EZ FONTOS!
            )
            # ... a többi maradhat ...
            for ploc in PoleLocation.objects.filter(arena=arena):
                ArchivedPoleLocation.objects.create(
                    archived_arena=archived_arena,
                    pole_name=ploc.pole.name_en,
                    color=ploc.pole.color,
                    length=ploc.pole.length,
                    quantity=ploc.quantity
                )
                ploc.pole.number += ploc.quantity
                ploc.pole.save()
            for wloc in WingLocation.objects.filter(arena=arena):
                ArchivedWingLocation.objects.create(
                    archived_arena=archived_arena,
                    wing_name=wloc.wing.name_en,
                    color=wloc.wing.color,
                    quantity=wloc.quantity
                )
                wloc.wing.number += wloc.quantity
                wloc.wing.save()
        event.is_archived = True
        event.is_active = False
        event.save()
        return Response({'detail': 'Event archived, all stock returned to warehouse.'})

    @action(detail=True, methods=['get'])
    def all_wishlists(self, request, pk=None):
        event = self.get_object()
        arenas = Arena.objects.filter(event=event)
        data = []
        for arena in arenas:
            wishlists = Wishlist.objects.filter(arena=arena)
            data.append({
                "arena": {
                    "id": arena.id,
                    "name": arena.name,
                },
                "wishlists": WishlistSerializer(wishlists, many=True).data
            })
        return Response({
            "event": event.name,
            "arenas": data
        })

class ArenaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCrewOrAdmin]
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
    permission_classes = [IsCrewOrAdmin]
    queryset = ArchivedEvent.objects.all()
    serializer_class = ArchivedEventDetailSerializer

class ArchivedEventViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsCrewOrAdmin]
    queryset = ArchivedEvent.objects.all()
    serializer_class = ArchivedEventDetailSerializer

class ActiveArenaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArenaSerializer
    queryset = Arena.objects.all()
    def get_queryset(self):
        # Lekérjük az összes archivált aréna "original_arena_id"-ját
        archived_ids = ArchivedArena.objects.values_list('original_arena_id', flat=True)
        # Csak azok az arénák, amik nincsenek archiválva, ÉS az eventjük aktív/élő
        return Arena.objects.exclude(id__in=archived_ids).filter(event__is_active=True, event__is_archived=False)