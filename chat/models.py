from django.db import models

# Stats Table: holds stats for each VOD entered
class Stats(models.Model):
    # Video Id
    VOD = models.CharField(max_length=1000, unique=True)
    
    # Name of the streamer
    streamerName = models.CharField(max_length=1000)

    # Number of positive comments
    positiveComments = models.BigIntegerField(blank=True, null=True)

    # Number of negative comments
    negativeComments = models.BigIntegerField(blank=True, null=True)

    # Number of neutral comments
    neutralComments = models.BigIntegerField(blank=True, null=True)

    # Streamer Thumbnails
    streamerThumbnail = models.CharField(max_length=1000, blank=True, null=True)

    # Most common word
    mostCommonWord = models.CharField(max_length=1000)

    # Most positive User
    mostPositiveUser = models.CharField(max_length=1000)

    # Most negative User
    mostNegativeUser = models.CharField(max_length=1000)

    # String representation of object
    def __str__(self):
        return self.VOD
