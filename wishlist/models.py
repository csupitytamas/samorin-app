from django.db import models
from django.contrib.auth.models import User
from events.models import Arena           # vagy ahova az Arena modelled van téve
from warehouse.models import Pole, Wings  # vagy amilyen nevű az eszköz modelled

class Wishlist(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    arena = models.ForeignKey(Arena, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Kívánságlista: {self.arena.name} - {self.created_by}"

class WishlistPoleItem(models.Model):
    MODE_CHOICES = (
        ('in', 'Warehouse in'),
        ('out', 'Arena out'),
    )
    wishlist = models.ForeignKey(Wishlist, related_name='pole_items', on_delete=models.CASCADE)
    pole = models.ForeignKey(Pole, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    mode = models.CharField(max_length=3, choices=MODE_CHOICES, default='in')

    def __str__(self):
        return f"{self.quantity} db {self.pole.name_hu} ({self.pole.color}) - {self.mode}"

class WishlistWingItem(models.Model):
    MODE_CHOICES = (
        ('in', 'Warehouse in'),
        ('out', 'Arena out'),
    )
    wishlist = models.ForeignKey(Wishlist, related_name='wing_items', on_delete=models.CASCADE)
    wing = models.ForeignKey(Wings, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    mode = models.CharField(max_length=3, choices=MODE_CHOICES, default='in')

    def __str__(self):
        return f"{self.quantity} db {self.wing.name_hu} ({self.wing.color}) - {self.mode}"