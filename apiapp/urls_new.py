from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    index
)

urlpatterns = [
    path('', index, name='index'),
]
