from rest_framework import routers
from django.urls import path, include 
from .views import ReservaViewSet, ReservaCadeiraViewSet

# Router para reservas de sala
router = routers.DefaultRouter()
router.register(r'', ReservaViewSet, basename='reserva')

# Router para reservas de cadeira (rota específica)
router_cadeira = routers.DefaultRouter()
router_cadeira.register(r'', ReservaCadeiraViewSet, basename='reserva-cadeira')

urlpatterns = [
    path('cadeira/', include(router_cadeira.urls)),  # /api/reservas/cadeira/
    path('', include(router.urls)),  # /api/reservas/
]