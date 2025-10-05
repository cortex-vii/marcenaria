from django.contrib import admin
from unfold.admin import ModelAdmin
from marcenaria.models import Ambiente

@admin.register(Ambiente)
class AmbienteAdmin(ModelAdmin):
    list_display = ['nome', 'orcamento', 'get_total_moveis', 'created_at', 'updated_at']
    list_filter = ['orcamento__status', 'created_at', 'updated_at']
    search_fields = ['nome', 'descricao', 'orcamento__numero', 'orcamento__cliente']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'orcamento'),
            'classes': ('wide',)
        }),
        ('Descrição', {
            'fields': ('descricao',),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Filtros no sidebar
    list_per_page = 25
    
    # Ordenação padrão
    ordering = ['-created_at']
    
    # Campos para busca avançada
    autocomplete_fields = ['orcamento']
    
    def get_total_moveis(self, obj):
        """Retorna o total de móveis no ambiente"""
        return obj.moveis.count()
    get_total_moveis.short_description = 'Total de Móveis'
    get_total_moveis.admin_order_field = 'moveis__count'
    
    def get_queryset(self, request):
        """Otimiza as consultas"""
        queryset = super().get_queryset(request)
        return queryset.select_related('orcamento').prefetch_related('moveis')
    
    # Ações personalizadas
    actions = ['duplicate_ambiente']
    
    def duplicate_ambiente(self, request, queryset):
        """Duplica ambientes selecionados"""
        duplicated_count = 0
        for ambiente in queryset:
            # Criar cópia do ambiente
            ambiente_copy = Ambiente.objects.create(
                orcamento=ambiente.orcamento,
                nome=f"{ambiente.nome} (Cópia)",
                descricao=ambiente.descricao
            )
            duplicated_count += 1
        
        self.message_user(
            request,
            f"{duplicated_count} ambiente(s) duplicado(s) com sucesso."
        )
    duplicate_ambiente.short_description = "Duplicar ambientes selecionados"