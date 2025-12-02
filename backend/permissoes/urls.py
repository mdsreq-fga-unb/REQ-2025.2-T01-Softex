from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PerfilPermissaoViewSet, UsuarioGerenciamentoViewSet

router = DefaultRouter()

router.register(r'perfis', PerfilPermissaoViewSet, basename='perfil-permissao')

router.register(r'usuarios-gerenciamento', UsuarioGerenciamentoViewSet, basename='usuario-gerenciamento')

urlpatterns = [
    path('', include(router.urls)),
]