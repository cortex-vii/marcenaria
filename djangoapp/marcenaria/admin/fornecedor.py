from django.contrib import admin
from unfold.admin import ModelAdmin
from marcenaria.models import Fornecedor

@admin.register(Fornecedor)
class FornecedorAdmin(ModelAdmin):
    list_display = ['nome', 'cnpj', 'telefone', 'email', 'ativo', 'created_at']
    list_filter = ['ativo', 'created_at']
    search_fields = ['nome', 'cnpj', 'contato', 'email', 'telefone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'cnpj', 'ativo')
        }),
        ('Contato', {
            'fields': ('contato', 'telefone', 'email')
        }),
        ('Endereço', {
            'fields': ('endereco',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )