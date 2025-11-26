from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import PermissionDenied
from .models import Cadastro

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email', '')
        if not Cadastro.objects.filter(email=email).exists():
            raise PermissionDenied("Email não autorizado")