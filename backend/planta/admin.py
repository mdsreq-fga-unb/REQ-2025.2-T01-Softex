from django.contrib import admin
from .models import Planta

@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = ('id_planta', 'nome', 'cadastro', 'mapa_imagem')
    # Adiciona 'cadastro' (o usuário que registrou a planta) aos filtros
    list_filter = ('cadastro',)
    search_fields = ('nome',)