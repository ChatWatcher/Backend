# Imports 
from django.urls import include, path
from rest_framework import routers
from . import views

# Create a router and register our viewsets with it.
router = routers.DefaultRouter()

# Returns the stats for the VOD specified by the VOD_ID
router.register(r'', views.ChatViewSet, basename='chat')

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('stats/', include(router.urls)),
]