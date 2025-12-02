from django.contrib import admin
from .models import Cadeira

@admin.register(Cadeira)
class CadeiraAdmin(admin.ModelAdmin):
    list_display = ('id_cadeira', 'sala', 'status', 'pos_x', 'pos_y')
    # Filtra por status e sala (ForeignKey)
    list_filter = ('status', 'sala')
    search_fields = ('sala__nome_sala',) # Permite buscar pelo nome da sala
    # Permite editar a posição diretamente na lista
    list_editable = ('status', 'pos_x', 'pos_y')