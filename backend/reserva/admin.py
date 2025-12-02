from django.contrib import admin
from .models import Reserva, ReservaCadeira

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id_reserva', 'usuario', 'sala', 'data_inicio', 'data_fim', 'status')
    list_filter = ('status', 'data_inicio')
    search_fields = ('usuario__email', 'sala__nome_sala')
    readonly_fields = ('data_criacao', 'data_modificacao')

@admin.register(ReservaCadeira)
class ReservaCadeiraAdmin(admin.ModelAdmin):
    list_display = ('id_reserva_cadeira', 'usuario', 'cadeira', 'data_inicio', 'hora_inicio', 'hora_fim', 'status')
    list_filter = ('status', 'data_inicio')
    search_fields = ('usuario__email', 'cadeira__id_cadeira')
    readonly_fields = ('data_criacao', 'data_modificacao')
