from django.contrib import admin
from .models import Cadastro

@admin.register(Cadastro)
class CadastroAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'tipo_permissao')
    search_fields = ('username', 'email')