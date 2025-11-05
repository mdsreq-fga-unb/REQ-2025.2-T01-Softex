from rest_framework import routers
from django.urls import path, include 
from .views import SalaViewSet

router = routers.DefaultRouter()
router.register(r'',SalaViewSet, basename='sala')

urlpatterns = [
    path('', include(router.urls)),
]