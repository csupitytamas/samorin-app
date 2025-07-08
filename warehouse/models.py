from django.db import models

class Warehouse(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Pole(models.Model):
    name_hu = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    length = models.FloatField(help_text="Length in meters")
    picture = models.ImageField(upload_to='pole_pics/', null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='poles')

    def __str__(self):
        return f"{self.name_en} ({self.color}, {self.length}m)"

class Wings(models.Model):
    name_hu = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='wing_pics/', null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='wings')

    def __str__(self):
        return f"{self.name_en} ({self.color})"