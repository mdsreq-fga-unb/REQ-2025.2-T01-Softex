"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from planta.views import PlantaViewSet
from cadastro.views import CadastroViewSet, login_view, google_login_redirect, google_callback, check_auth
from sala.views import SalaViewSet, SalaDeReuniaoViewSet
from cadeira.views import CadeiraViewSet

router = DefaultRouter()

# Regista 'api/plantas/'
router.register(r'plantas', PlantaViewSet, basename='planta')

# Regista 'api/cadastro/'
router.register(r'cadastro', CadastroViewSet, basename='cadastro')

# Regista 'api/salas/'
router.register(r'salas', SalaViewSet, basename='sala')
router.register(r'salas-reuniao', SalaDeReuniaoViewSet, basename='sala-de-reuniao')

# Regista 'api/cadeiras/'
router.register(r'cadeiras', CadeiraViewSet, basename='cadeira')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/reservas/', include('reserva.urls')),  # Rotas de reserva
    path('api/auth/google/login/', google_login_redirect, name='google-login-redirect'),  # Inicia OAuth2
    path('api/auth/google/callback/', google_callback, name='google-callback'),  # Callback OAuth2
    path('api/auth/check/', check_auth, name='check-auth'),  # Verificar autenticação
    path('api/login/', login_view, name='login'),  # Login tradicional (backup)
]

# so adiciona documentos de imagem em modo debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)