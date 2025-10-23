from rest_framework import routers
from .views import CadastroViewSet

router = routers.DefaultRouter()
router.register(r'cadastros', CadastroViewSet)

urlpatterns = router.urls
