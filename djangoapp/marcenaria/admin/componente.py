from django.contrib import admin
from unfold.admin import ModelAdmin
from marcenaria.models import Componente
import locale

@admin.register(Componente)
class ComponenteAdmin(ModelAdmin):
    list_display = ['nome', 'tipo_componente', 'fornecedor', 'unidade_medida', 'get_preco_bruto', 'get_custo_unitario', 'updated_at']
    list_filter = ['unidade_medida', 'fornecedor', 'tipo_componente']
    search_fields = ['nome', 'tipo_componente__nome', 'fornecedor__nome']
    readonly_fields = ['created_at', 'updated_at', 'get_custo_unitario_readonly']
    
    autocomplete_fields = ['tipo_componente', 'fornecedor']
    
    fieldsets = (
        ('Informações do Componente', {
            'fields': ('nome', 'tipo_componente', 'fornecedor', 'unidade_medida', 'preco_bruto'),
            'classes': ('wide',)
        }),
        ('📐 METRO QUADRADO (m²)', {
            'fields': (('altura', 'largura', 'profundidade'),),
            'classes': ('wide',),
            'description': '<strong>Preencher APENAS se a unidade de medida for "Metro Quadrado"</strong><br>'
                          'Altura e largura são obrigatórios. Profundidade é opcional (para volumes).'
        }),
        ('📏 METRO LINEAR (m)', {
            'fields': ('comprimento',),
            'classes': ('wide',),
            'description': '<strong>Preencher APENAS se a unidade de medida for "Metro Linear"</strong><br>'
                          'Informe o comprimento em metros.'
        }),
        ('🧪 LÍQUIDOS (ml)', {
            'fields': ('volume_ml',),
            'classes': ('wide',),
            'description': '<strong>Preencher APENAS se a unidade de medida for "Mililitros"</strong><br>'
                          'Informe o volume em mililitros.'
        }),
        ('🔢 UNIDADES', {
            'fields': ('quantidade',),
            'classes': ('wide',),
            'description': '<strong>Preencher APENAS se a unidade de medida for "Unidade"</strong><br>'
                          'Informe a quantidade de itens.'
        }),
        ('💰 Custo Calculado', {
            'fields': ('get_custo_unitario_readonly',),
            'classes': ('wide',),
            'description': 'Calculado automaticamente ao salvar: preço bruto ÷ (dimensões × quantidade)'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    list_per_page = 25
    ordering = ['-created_at']

    def format_currency(self, value):
        """Formata valor com vírgula ao invés de ponto"""
        return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    @admin.display(description='Preço Bruto')
    def get_preco_bruto(self, obj):
        return self.format_currency(obj.preco_bruto)

    @admin.display(description='Custo Unitário')
    def get_custo_unitario(self, obj):
        unidade_texto = {
            'QUADRADO': '/m²',
            'LINEAR': '/m',
            'LIQUIDO': '/ml',
            'UNIDADE': '/un'
        }.get(obj.unidade_medida, '')
        
        valor_formatado = f"{obj.custo_unitario:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return f"R$ {valor_formatado}{unidade_texto}"

    @admin.display(description='Custo por m²/m/ml/unidade')
    def get_custo_unitario_readonly(self, obj):
        """Versão readonly para o fieldset"""
        return self.get_custo_unitario(obj)

    class Media:
        css = {
            'all': ('admin/css/componente_admin.css',)
        }