from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cadastro # Importa seu modelo customizado

@admin.register(Cadastro)
class CadastroAdmin(UserAdmin):
    # Adapta a visualização do usuário para incluir seu campo customizado
    list_display = (
        'email', 
        'username', 
        'first_name', 
        'last_name', 
        'tipo_funcao', 
        'is_staff'
    )
    # Permite a edição do campo tipo_funcao no formulário de detalhes
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('tipo_funcao',)}),
    )
    # Adiciona tipo_funcao aos filtros de lista
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'tipo_funcao')
    search_fields = ('email', 'first_name', 'last_name')