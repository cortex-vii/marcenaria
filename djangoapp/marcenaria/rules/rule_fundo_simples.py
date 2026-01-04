from .calc_tipos_componentes.calc_mdf import calcular_custo_mdf
from marcenaria.utils.data_format import format_decimal
from .calc_tipos_componentes.calc_parafusos import calcular_parafusos_fundo_simples


class FundoSimplesRule:
    """Classe com as regras para calcular Fundo Simples"""
    
    # Componentes que esta peça pode usar
    COMPONENTES_DISPONIVEIS = ['AC-001']  # MDF
    COMPONENTES_ADICIONAIS = ['AC-006']   # Parafusos
    
    # Mapeamento de códigos de tipo de componente para funções de cálculo
    CALCULADORAS_ADICIONAIS = {
        'AC-006': calcular_parafusos_fundo_simples,  # Parafusos com regra específica
    }
    
    # Campos necessários para o cálculo
    CAMPOS_NECESSARIOS = [
        {
            'name': 'quantidade',
            'label': 'Quantidade de peças',
            'type': 'number',
            'required': True,
            'min': 1,
            'help': 'Quantas peças de fundo simples você precisa'
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
        },
    ]
    
    @staticmethod
    def calcular(dados, componente, componentes_adicionais=None):
        """
        Calcula a quantidade de material necessária para fundo simples
        
        Args:
            dados (dict): Dicionário com quantidade, altura, largura
            componente (Componente): Componente principal (MDF)
            componentes_adicionais (list): Lista de componentes adicionais (parafusos)
            
        Returns:
            dict: Resultado do cálculo
        """
        # Cálculo MDF (principal)
        resultado_mdf = calcular_custo_mdf(dados, componente)
        if resultado_mdf.get('erro'):
            return {'erro': resultado_mdf['erro']}

        def parse_float(val):
            if isinstance(val, str):
                return float(val.replace(',', '.'))
            return float(val)

        area_total = parse_float(resultado_mdf['quantidade_utilizada'])
        quantidade = float(dados.get('quantidade', 0))
        altura = float(dados.get('altura', 0))
        largura = float(dados.get('largura', 0))

        custo_adicionais = 0
        detalhes_adicionais = []
        if componentes_adicionais:
            for comp in componentes_adicionais:
                # Buscar a função de cálculo apropriada para o tipo do componente
                codigo_tipo = comp.tipo_componente.codigo if hasattr(comp, 'tipo_componente') else None
                
                if codigo_tipo and codigo_tipo in FundoSimplesRule.CALCULADORAS_ADICIONAIS:
                    funcao_calculo = FundoSimplesRule.CALCULADORAS_ADICIONAIS[codigo_tipo]
                    resultado = funcao_calculo(dados, comp)
                    
                    if not resultado.get('erro'):
                        custo_adicionais += parse_float(resultado['custo_total'])
                        detalhes_adicionais.append(resultado)
                    else:
                        print(f"Erro ao calcular {comp.nome}: {resultado.get('erro')}")
                else:
                    print(f"Aviso: Componente adicional '{comp.nome}' (tipo: {codigo_tipo}) não tem calculadora definida")

        custo_total = parse_float(resultado_mdf['custo_total']) + custo_adicionais
        return {
            'sucesso': True,
            'area_por_peca': resultado_mdf['area_por_peca'] if 'area_por_peca' in resultado_mdf else resultado_mdf['quantidade_utilizada'],
            'area_total': area_total,
            'quantidade_utilizada': resultado_mdf['quantidade_utilizada'],
            'unidade': resultado_mdf.get('unidade', 'm²'),
            'custo_total': f"{custo_total:.2f}",
            'detalhes': [
                {
                    'componente': componente.nome,
                    'tipo': 'principal',
                    'quantidade': resultado_mdf['quantidade_utilizada'],
                    'unidade': resultado_mdf.get('unidade', 'm²'),
                    'custo': resultado_mdf['custo_total'],
                    'resumo': resultado_mdf['resumo']
                },
                *detalhes_adicionais
            ],
            'resumo': f"{dados.get('quantidade')}x peças de {dados.get('altura')}cm x {dados.get('largura')}cm = {resultado_mdf['quantidade_utilizada']} m²"
        }