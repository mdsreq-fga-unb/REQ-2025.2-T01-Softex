from rest_framework import routers
from django.urls import path, include 
from .views import SalaViewSet, SalaDeReuniaoViewSet

router = routers.DefaultRouter()
router.register(r'',SalaViewSet, basename='sala')
router.register(r'salas-reuniao', SalaDeReuniaoViewSet, basename='sala-de-reuniao')

urlpatterns = [
    path('', include(router.urls)),
]