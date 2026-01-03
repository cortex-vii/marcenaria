from .calc_tipos_componentes.calc_fita import calcular_custo_fita
from .calc_tipos_componentes.calc_mdf import calcular_custo_mdf
from ..utils.data_format import format_decimal

class BaseSimplesRule:
    """Classe com as regras para calcular Base Simples"""
    
    # Componentes que esta peça pode usar
    COMPONENTES_DISPONIVEIS = ['AC-001']  # MDF
    COMPONENTES_ADICIONAIS = ["AC-002"]   # Fita
    
    # Campos necessários para o cálculo
    CAMPOS_NECESSARIOS = [
        {
            'name': 'quantidade',
            'label': 'Quantidade de peças',
            'type': 'number',
            'required': True,
            'min': 1,
            'help': 'Quantas peças de base simples você precisa'
        },
        {
            'name': 'altura',
            'label': 'Altura (cm)',
            'type': 'number',
            'required': True,
            'min': 0.1,
            'step': 0.1,
            'help': 'Altura da peça em centímetros'
        },
        {
            'name': 'largura',
            'label': 'Largura (cm)',
            'type': 'number',
            'required': True,
            'min': 0.1,
            'step': 0.1,
            'help': 'Largura da peça em centímetros'
        }
    ]
    
    @staticmethod
    def calcular(dados, componente, componentes_adicionais=None):
        print("\n========== CALCULANDO BASE SIMPLES ==========")
        print("ID do componente principal:", componente.id)
        print("IDs dos componentes adicionais:", componentes_adicionais)
        print("===========================================\n")

        # Cálculo MDF (principal)
        resultado_mdf = calcular_custo_mdf(dados, componente)
        if resultado_mdf.get('erro'):
            return {'erro': resultado_mdf['erro']}

        def parse_float(val):
            if isinstance(val, str):
                return float(val.replace(',', '.'))
            return float(val)

        area_por_peca = parse_float(resultado_mdf['quantidade_utilizada']) / float(dados.get('quantidade', 1))
        area_total = parse_float(resultado_mdf['quantidade_utilizada'])
        quantidade = float(dados.get('quantidade', 0))
        altura = float(dados.get('altura', 0))
        largura = float(dados.get('largura', 0))

        custo_adicionais = 0
        detalhes_adicionais = []
        if componentes_adicionais:
            for comp in componentes_adicionais:
                if comp.nome.upper().startswith('FITA'):
                    resultado_fita = calcular_custo_fita(dados, comp)
                    custo_adicionais += resultado_fita['custo_total']
                    detalhes_adicionais.append(resultado_fita)

        custo_total = resultado_mdf['custo_total'] + custo_adicionais

        return {
            'sucesso': True,
            'area_por_peca': format_decimal(area_por_peca),
            'area_total': format_decimal(area_total),
            'quantidade_utilizada': format_decimal(area_total),
            'unidade': 'm²',
            'custo_total': format_decimal(custo_total),
            'detalhes': [
                {
                    'componente': componente.nome,
                    'tipo': 'principal',
                    'quantidade': format_decimal(area_total),
                    'unidade': 'm²',
                    'custo': format_decimal(resultado_mdf['custo_total']),
                    'resumo': resultado_mdf['resumo']
                },
                *detalhes_adicionais
            ],
            'resumo': f"{format_decimal(quantidade)}x peças de {format_decimal(altura)}cm x {format_decimal(largura)}cm = {format_decimal(area_total)} m²"
        }