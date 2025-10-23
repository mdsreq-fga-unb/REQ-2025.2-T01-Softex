from django.shortcuts import render
from rest_framework import viewsets
from .models import Cadastro
from .serializers import CadastroSerializer

class CadastroViewSet(viewsets.ModelViewSet):
    queryset = Cadastro.objects.all()
    serializer_class = CadastroSerializer