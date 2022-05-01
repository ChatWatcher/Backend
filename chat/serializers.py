# Imports
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from rest_framework import serializers

from .models import Stats

# Abstraction is integrated due to django within all of these classes
class StatSerializer(serializers.ModelSerializer):
    class Meta:
        # Database table
        model = Stats
        # Fields to appear on the response
        fields = ('VOD', 'streamerName', 'positiveComments', 'negativeComments', 'neutralComments', 'streamerThumbnail', 'mostCommonWord', 'mostPositiveUser', 'mostNegativeUser', )

