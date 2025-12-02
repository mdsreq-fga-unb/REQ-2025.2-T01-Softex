from django.contrib import admin
from .models import Reserva

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'id_reserva', 
        'usuario', 
        'sala', 
        'data_inicio', 
        'data_fim', 
        'status'
    )
    # Filtra por status, usuário e sala
    list_filter = ('status', 'usuario', 'sala', 'data_inicio')
    search_fields = ('usuario__email', 'sala__nome_sala', 'descricao')
    # Exibe datas de criação e modificação apenas no detalhe
    readonly_fields = ('data_criacao', 'data_modificacao')