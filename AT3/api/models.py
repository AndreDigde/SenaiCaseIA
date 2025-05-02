from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Prediction(models.Model):
    prediction_id = models.AutoField(primary_key=True)
    relative_compactness = models.FloatField()
    surface_area = models.FloatField()
    wall_area = models.FloatField()
    roof_area = models.FloatField()
    overall_height = models.FloatField()
    orientation = models.IntegerField()
    glazing_area = models.FloatField()
    glazing_area_distribution = models.IntegerField()
    heating_load = models.FloatField()
    colding_load = models.FloatField()


class User(AbstractUser):
    REQUIRED_FIELDS = ['password']
    USERNAME_FIELD = 'username'
