from django.shortcuts import render
from rest_framework import viewsets
from .models import Planta
from .serializers import PlantaSerializer

class PlantaViewSet(viewsets.ModelViewSet):
    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer
    

