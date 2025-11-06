from rest_framework import routers
from django.urls import path, include 
from .views import ReservaViewSet

router = routers.DefaultRouter()
router.register(r'', ReservaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]