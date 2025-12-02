"""
Middleware para desabilitar CSRF em rotas de API
"""
from django.utils.deprecation import MiddlewareMixin

class DisableCSRFForAPI(MiddlewareMixin):
    """
    Desabilita verificação de CSRF para rotas de API
    """
    def process_request(self, request):
        # Desabilitar CSRF para todas as rotas que começam com /api/
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)

