from django.db import models

# Create your models here.
class Stats(models.Model):
    VOD = models.CharField(max_length=150)
    author = models.CharField(max_length=100)