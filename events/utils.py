# events/utils.py
from .models import Event, ArchivedEvent, Arena, ArchivedArena, PoleLocation, WingLocation, ArchivedPoleLocation, ArchivedWingLocation
from django.utils import timezone

def archive_event(event):
    if event.is_archived:
        return
    archived_event = ArchivedEvent.objects.create(
        event=event,
        closed_at=timezone.now()
    )
    for arena in Arena.objects.filter(event=event):
        archived_arena = ArchivedArena.objects.create(
            archived_event=archived_event,
            name=arena.name,
            original_arena_id=arena.id
        )
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
