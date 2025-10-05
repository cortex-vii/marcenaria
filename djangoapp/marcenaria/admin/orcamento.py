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
    list_display = ['numero', 'cliente', 'status', 'get_total_ambientes', 'data_validade', 'created_at', 'updated_at']
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
        ('valor_total', {
            'fields': ('valor_total',),
        }),
  
    )

    list_per_page = 25
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    inlines = [AmbienteInline]

    # Redireciona o botão "Adicionar" do admin para a sua view manual
    def add_view(self, request, form_url='', extra_context=None):
        return redirect('marcenaria:orcamento_create')

    def get_total_ambientes(self, obj):
        """Retorna o total de ambientes no orçamento"""
        return obj.ambientes.count()
    get_total_ambientes.short_description = 'Total de Ambientes'
    get_total_ambientes.admin_order_field = 'ambientes__count'

    def get_queryset(self, request):
        """Otimiza as consultas"""
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('ambientes')

