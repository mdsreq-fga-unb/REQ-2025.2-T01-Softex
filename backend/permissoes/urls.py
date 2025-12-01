from rest_framework.routers import DefaultRouter
from django.urls import path, include  # <-- FALTAVA ISSO
from .views import PerfilPermissaoViewSet

router = DefaultRouter()
router.register(r'perfis', PerfilPermissaoViewSet, basename='perfil-permissao')

urlpatterns = [
    path('', include(router.urls)),
]