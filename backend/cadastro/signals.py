from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.contrib import messages
from django.shortcuts import redirect
from .models import Cadastro

@receiver(pre_social_login)
def limit_google_login(sender, request, sociallogin, **kwargs):
    email = sociallogin.account.extra_data.get('email', '')

    if not Cadastro.objects.filter(email=email).exists():
        # "Cancela" o login
        sociallogin.state = None
        messages.error(request, "Email não autorizado para login.")
        raise Exception("Email não autorizado")  # força a parar