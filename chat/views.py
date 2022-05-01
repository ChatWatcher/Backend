# Imports
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters

from .serializers import StatSerializer
from .models import Stats

from .scripts.main import main as createStat

import re

class ChatViewSet(viewsets.ModelViewSet):
    # Permission needed to access endpoint
    permission_classes = (permissions.AllowAny,)
    # URL parameter passed into url that also exists in the CongressTrade and CongressPerson models 
    lookup_field = 'VOD'
    # Initiliazing our seializer class
    serializer_class = StatSerializer
        
    # filter by slug in url in django rest framework modelviewset
    def get_queryset(self):
        # Get the name that was passed in the URL
        # VOD = self.kwargs['VOD']
        url = self.request.query_params.get('VOD')

        if "https" in url:
            # VOD ID - parse from end of string, or question mark to last slash
            if "?" not in url:    
                # Twitch
                VOD = url.rsplit('/', 1)[1]
            else:
                # match regex expression
                VOD = re.search(".*\/(.*)\?", url).group(1)

        # Query Database for the name
        queryset = Stats.objects.filter(VOD=VOD)

        
        # If queryset is empty 
        if len(queryset) == 0:
            print("here")
            # run script to get data from twitch api
            VOD = createStat(url)
    
            queryset = Stats.objects.filter(VOD=VOD)


        return queryset
