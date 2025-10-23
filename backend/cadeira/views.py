from django.shortcuts import render
from rest_framework import viewsets
from .models import Cadeira
from .serializers import CadeiraSerializer


class CadeiraViewSet(viewsets.ModelViewSet):
    #define o objeto que a view vai  manipular 
    queryset = Cadeira.objects.all()        
    
    #define qual serializer vai ser usado
    serializer_class = CadeiraSerializer

