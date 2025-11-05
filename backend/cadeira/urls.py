from rest_framework import routers
from django.urls import path, include 
from .views import CadeiraViewSet

router = routers.DefaultRouter()
router.register(r'', CadeiraViewSet, basename='cadeira')

urlpatterns = [
    path('', include(router.urls)),
]