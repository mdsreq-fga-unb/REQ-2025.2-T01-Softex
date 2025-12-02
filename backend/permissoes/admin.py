from django.contrib import admin
from .models import PerfilDePermissao # Importa a nova model

@admin.register(PerfilDePermissao)
class PerfilDePermissaoAdmin(admin.ModelAdmin):
    # Campos exibidos na lista principal do Admin
    list_display = (
        'nome', 
        'acessoBasico', 
        'dashboards', 
        'salasReuniao', 
        'administracao'
    )
    # Campos que podem ser usados para filtrar a lista
    list_filter = ('acessoBasico', 'dashboards', 'administracao')
    # Campos usados na busca
    search_fields = ('nome', 'descricao')