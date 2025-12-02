# sala/admin.py
from django.contrib import admin
from .models import Sala, SalaDeReuniao

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('id_sala', 'nome_sala', 'tipo', 'capacidade', 'planta')
    list_filter = ('tipo', 'planta')
    search_fields = ('nome_sala',)


@admin.register(SalaDeReuniao)
class SalaDeReuniaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)
