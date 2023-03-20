# Imports
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings

# Auto Documentation Imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Creating Documentation for the API
schema_view = get_schema_view(
   openapi.Info(
      title="Chat Watch",
      default_version='v1',
      description="Chat Watch API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="rehmafar@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Security feature - Honeypot Admin: fake login page which records the ip and attempeted username and password 
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),

    # Real admin page 
    path('secretadmin/', admin.site.urls),

    # Imports the urls from the app chat/urls.py
    path('', include('chat.urls')),

    # Auto Documentation url
    url(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
