from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    Usuario,
    Permissao,
    Papel,
)

# ============ Usuario ============ #

@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    # Exibe campos essenciais na listagem, incluindo status e auditoria
    list_display = ['username', 'email', 'first_name', 'last_name', 'ativo', 'is_staff', 'created_at']
    list_filter = ['ativo', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    # Campos de auditoria protegidos contra edição manual
    readonly_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'last_login', 'date_joined']
    ordering = ['username']
    
    # Interface melhorada para selecionar muitos itens (N:N)
    filter_horizontal = ['papeis', 'permissoes_diretas', 'groups', 'user_permissions']

    # Organização do formulário em seções lógicas
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informacoes Pessoais', {'fields': ('first_name', 'last_name', 'email', 'pessoa_fisica')}),
        ('Permissoes', {
            'fields': ('ativo', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('RBAC', {
            'fields': ('papeis', 'permissoes_diretas'),
        }),
        ('Datas Importantes', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('ID', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )

    # Configuração para o formulário de "Adicionar Usuário"
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


# ============ Permissao ============ #

@admin.register(Permissao)
class PermissaoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'created_at']
    search_fields = ['codigo', 'nome', 'descricao']
    readonly_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
    ordering = ['codigo']

    fieldsets = (
        ('Dados da Permissao', {
            'fields': ('codigo', 'nome', 'descricao')
        }),
        ('Auditoria', {
            'fields': ('id', 'created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )


# ============ Papel ============ #

@admin.register(Papel)
class PapelAdmin(admin.ModelAdmin):
    list_display = ['nome', 'get_permissoes_count', 'created_at']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
    filter_horizontal = ['permissoes'] # Facilita a atribuição de muitas permissões
    ordering = ['nome']

    fieldsets = (
        ('Dados do Papel', {
            'fields': ('nome', 'descricao')
        }),
        ('Permissoes', {
            'fields': ('permissoes',)
        }),
        ('Auditoria', {
            'fields': ('id', 'created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )

    # Método auxiliar para mostrar a contagem na listagem
    def get_permissoes_count(self, obj):
        return obj.permissoes.count()
    get_permissoes_count.short_description = 'Qtd. Permissoes'