from django.urls import path, include
from rest_framework import routers
from .views import ReservaViewSet, ReservaCadeiraViewSet, DashboardStatsView

# Router principal com as novas rotas
router = routers.DefaultRouter()
router.register(r'reservas', ReservaViewSet, basename='reserva')
router.register(r'reservas-cadeira', ReservaCadeiraViewSet, basename='reserva-cadeira')

# Router de compatibilidade para manter as rotas antigas funcionando
router_compat = routers.DefaultRouter()
router_compat.register(r'', ReservaViewSet, basename='reserva-compat')

router_cadeira_compat = routers.DefaultRouter()
router_cadeira_compat.register(r'', ReservaCadeiraViewSet, basename='reserva-cadeira-compat')

urlpatterns = [
    # Rotas específicas primeiro (ordem importa no Django)
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('cadeira/', include(router_cadeira_compat.urls)),  # Mantém /api/reservas/cadeira/
    
    # Novas rotas: /api/reservas/reservas/ e /api/reservas/reservas-cadeira/
    path('', include(router.urls)),
    
    # Rota de compatibilidade para /api/reservas/ (lista de reservas) - deve vir por último
    path('', include(router_compat.urls)),
]