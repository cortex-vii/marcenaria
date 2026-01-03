from django.contrib import admin
from django.shortcuts import redirect
from unfold.admin import ModelAdmin, StackedInline
from marcenaria.models import Orcamento, Ambiente

class AmbienteInline(StackedInline):
    """Inline para ambientes dentro do orçamento"""
    model = Ambiente
    extra = 1
    fields = ['nome']
    classes = ('wide',)

@admin.register(Orcamento)
class OrcamentoAdmin(ModelAdmin):
    list_display = ['numero', 'cliente', 'status', 'get_total_ambientes', 'data_validade', 'created_at', 'updated_at','valor_total', 'visualizar_button']
    list_filter = ['status', 'data_validade', 'created_at', 'updated_at']
    search_fields = ['numero', 'cliente', 'descricao']
    readonly_fields = ['numero', 'created_at', 'updated_at', 'valor_total']

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('numero', 'cliente', 'status'),
            'classes': ('wide',)
        }),
        ('Detalhes', {
            'fields': ('descricao', 'data_validade'),
            'classes': ('wide',)
        }),
        ('Observações', {
            'fields': ('observacoes',),
            'classes': ('wide',)
        }),
        ('Valor total', {
            'fields': ('valor_total',),
        }),
        ('Dados do Orçamento', {
            'fields': ('dados_orcamento',),
        }),
        
  
    )

    list_per_page = 25
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    inlines = [AmbienteInline]

    # Redireciona o botão "Adicionar" do admin para a sua view manual
    def add_view(self, request, form_url='', extra_context=None):
        return redirect('marcenaria:orcamento_create')

    # Redireciona o clique no número do orçamento para a view customizada
    def change_view(self, request, object_id, form_url='', extra_context=None):
        return redirect('marcenaria:orcamento_edit', pk=object_id)

    def visualizar_button(self, obj):
        """Retorna um botão HTML para visualizar o orçamento"""
        from django.urls import reverse
        from django.utils.html import format_html
        
        url = reverse('marcenaria:orcamento_edit', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" style="padding: 5px 10px; background: #417690; color: white; text-decoration: none; border-radius: 4px;">📋 Visualizar</a>',
            url
        )
    visualizar_button.short_description = 'Ações'
    visualizar_button.allow_tags = True

    def get_total_ambientes(self, obj):
        """Retorna o total de ambientes no orçamento"""
        return obj.ambientes.count()
    get_total_ambientes.short_description = 'Total de Ambientes'
    get_total_ambientes.admin_order_field = 'ambientes__count'

    def get_queryset(self, request):
        """Otimiza as consultas"""
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('ambientes')

