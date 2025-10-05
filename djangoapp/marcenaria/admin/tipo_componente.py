from django.contrib import admin
from unfold.admin import ModelAdmin
from marcenaria.models import TipoComponente

@admin.register(TipoComponente)
class TipoComponenteAdmin(ModelAdmin):
    list_display = ['nome', 'ativo', 'created_at', 'updated_at']
    list_filter = ['ativo', 'created_at']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'ativo')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )