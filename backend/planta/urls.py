from rest_framework import routers
from django.urls import path, include
from .views import PlantaViewSet

router = routers.DefaultRouter()
router.register(r'Plantas', PlantaViewSet, basename='Plantas')

urlpatterns = [
    path('', include(router.urls)),
]