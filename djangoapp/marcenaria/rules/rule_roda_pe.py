from .calc_tipos_componentes.calc_roda import calcular_custo_mdf_roda, calcular_custo_fita_roda, calcular_parafusos_roda
from ..utils.data_format import format_decimal

class RodaPeRule:
    """Classe com as regras para calcular Roda Pé"""
    
    # Componentes que esta peça pode usar
    COMPONENTES_DISPONIVEIS = ['AC-001']  # MDF
    COMPONENTES_ADICIONAIS = ["AC-002", 'AC-006']   # Fita e Parafusos
    
    # Mapeamento de códigos de tipo de componente para funções de cálculo
    CALCULADORAS_ADICIONAIS = {
        'AC-002': calcular_custo_fita_roda,      # Fita com regra específica
        'AC-006': calcular_parafusos_roda,  # Parafusos com regra específica
    }
    
    # Campos necessários para o cálculo
    CAMPOS_NECESSARIOS = [
        {
            'name': 'quantidade',
            'label': 'Quantidade de peças',
            'type': 'number',
            'required': True,
            'min': 1,
            'help': 'Quantas peças de roda pé você precisa'
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
        {
            'name': 'profundidade',
            'label': 'Profundidade (cm)',
            'type': 'number',
            'required': True,
            'min': 0.1,
            'step': 0.1,
            'help': 'Profundidade da peça em centímetros'
        }
    ]
    
    @staticmethod
    def calcular(dados, componente, componentes_adicionais=None):
        """
        Calcula a quantidade de material necessária para roda pé
        
        Args:
            dados (dict): Dicionário com quantidade, altura, largura, profundidade
            componente (Componente): Componente principal (MDF)
            componentes_adicionais (list): Lista de componentes adicionais (fita, parafusos)
            
        Returns:
            dict: Resultado do cálculo
        """
        # Cálculo MDF (principal) usando função específica para roda
        resultado_mdf = calcular_custo_mdf_roda(dados, componente)
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
        profundidade = float(dados.get('profundidade', 0))

        custo_adicionais = 0
        detalhes_adicionais = []
        if componentes_adicionais:
            for comp in componentes_adicionais:
                # Buscar a função de cálculo apropriada para o tipo do componente
                codigo_tipo = comp.tipo_componente.codigo if hasattr(comp, 'tipo_componente') else None
                
                if codigo_tipo and codigo_tipo in RodaPeRule.CALCULADORAS_ADICIONAIS:
                    funcao_calculo = RodaPeRule.CALCULADORAS_ADICIONAIS[codigo_tipo]
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
            'area_por_peca': parse_float(resultado_mdf['quantidade_utilizada']) / quantidade if quantidade > 0 else 0,
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
            'resumo': f"{quantidade}x peças de roda pé de {altura}cm x {largura}cm x {profundidade}cm = {resultado_mdf['quantidade_utilizada']} m²"
        }