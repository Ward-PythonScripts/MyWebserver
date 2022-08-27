from tkinter import CASCADE
from django.db import models

# Create your models here.

class Track(models.Model):
    begin_date = models.DateField
    end_date = models.DateField
    layout_image = models.ImageField

class Driver(models.Model):
    driver_name = models.CharField(max_length=50)


class Session(models.Model):
    session_day = models.DateField
    track_id = models.ForeignKey(Track, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver,on_delete=models.DO_NOTHING)

class Lap(models.Model):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    laptime = models.DecimalField(decimal_places=3,max_digits=6)
    lap_of_session = models.PositiveSmallIntegerField()


