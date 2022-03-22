from django.db import models

# Create your models here.
class ElevationQuery(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    elevation = models.FloatField(blank=True)

    def __str__(self):
        if self.is_valid:
            return f"{self.lat}, {self.lon}, {self.elevation}"
        return f"{self.lat}, {self.lon}"

class DistanceQuery(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    lat1 = models.FloatField(default=0)
    lon1 = models.FloatField(default=0)
    lat2 = models.FloatField(default=0)
    lon2 = models.FloatField(default=0)
    dist = models.FloatField(blank=True)

    def __str__(self):
        return f"""({self.lat1},{self.lon1}), 
            ({self.lat2},{self.lon2}), {self.dist}"""
