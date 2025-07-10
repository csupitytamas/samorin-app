from django.db import models
from django.contrib.auth.models import User
from warehouse.models import Pole, Wings, Warehouse

class Event(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Arena(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='arenas')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.event.name})"

class PoleLocation(models.Model):
    pole = models.ForeignKey(Pole, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    arena = models.ForeignKey('Arena', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        location = self.arena.name if self.arena else self.warehouse.name
        return f"{self.pole} x {self.quantity} @ {location}"

    def delete(self, *args, **kwargs):
        # warehouse készlet visszaállítása
        if self.pole:
            self.pole.number += self.quantity
            self.pole.save()
        super().delete(*args, **kwargs)

class WingLocation(models.Model):
    wing = models.ForeignKey(Wings, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    arena = models.ForeignKey('Arena', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        location = self.arena.name if self.arena else self.warehouse.name
        return f"{self.wing} x {self.quantity} @ {location}"

    def delete(self, *args, **kwargs):
        if self.wing:
            self.wing.number += self.quantity
            self.wing.save()
        super().delete(*args, **kwargs)


class ArchivedEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    closed_at = models.DateTimeField(auto_now_add=True)

class ArchivedArena(models.Model):
    original_arena_id = models.IntegerField(null=True, blank=True)
    archived_event = models.ForeignKey('ArchivedEvent', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class ArchivedPoleLocation(models.Model):
    archived_arena = models.ForeignKey(ArchivedArena, on_delete=models.CASCADE)
    pole_name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    length = models.FloatField()
    quantity = models.PositiveIntegerField()

class ArchivedWingLocation(models.Model):
    archived_arena = models.ForeignKey(ArchivedArena, on_delete=models.CASCADE)
    wing_name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
