from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_ROLES = (
        ('worker', 'Worker'),
        ('chief', 'Chief'),
        ('crew', 'Crew'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='worker')

    def __str__(self):
        return f"{self.user.username} ({self.role})"