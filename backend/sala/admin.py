from django.contrib import admin
from .models import Sala, TIPO_SALA_CHOICES # Importa Sala e as escolhas de tipo
from planta.models import Planta # Necessário para o ForeignKey

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('id_sala', 'nome_sala', 'tipo', 'capacidade', 'planta')
    # Filtra por tipo de sala (Estação ou Reunião)
    list_filter = ('tipo', 'capacidade', 'planta')
    search_fields = ('nome_sala', 'descricao')
    
    # Adiciona a descrição completa do tipo no formulário de edição
    fieldsets = (
        (None, {'fields': ('nome_sala', 'tipo', 'capacidade', 'descricao', 'planta')}),
    )