from rest_framework import routers
from django.urls import path, include 
from .views import CadastroViewSet

router = routers.DefaultRouter()
router.register(r'', CadastroViewSet)

router = routers.DefaultRouter()
router.register(r'',CadastroViewSet, basename='cadastro')

urlpatterns = [
    path('', include(router.urls)),
]