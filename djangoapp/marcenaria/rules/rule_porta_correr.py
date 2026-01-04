from .calc_tipos_componentes.calc_fita import calcular_custo_fita
from .calc_tipos_componentes.calc_mdf import calcular_custo_mdf
from ..utils.data_format import format_decimal

class PortaCorrerRule:
    """Classe com as regras para calcular Porta de Correr"""
    
    # Componentes que esta peça pode usar
    COMPONENTES_DISPONIVEIS = ['AC-001']  # MDF
    COMPONENTES_ADICIONAIS = ["AC-002"]   # Fita
    
    # Mapeamento de códigos de tipo de componente para funções de cálculo
    CALCULADORAS_ADICIONAIS = {
        'AC-002': calcular_custo_fita,      # Fita de borda
    }
    
    # Campos necessários para o cálculo
    CAMPOS_NECESSARIOS = [
        {
            'name': 'quantidade',
            'label': 'Quantidade de portas',
            'type': 'number',
            'required': True,
            'min': 1,
            'help': 'Quantas portas de correr você precisa'
        },
        {
            'name': 'altura',
            'label': 'Altura (cm)',
            'type': 'number',
            'required': True,
            'min': 0.1,
            'step': 0.1,
            'help': 'Altura da porta em centímetros'
        },
        {
            'name': 'largura',
            'label': 'Largura (cm)',
            'type': 'number',
            'required': True,
            'min': 0.1,
            'step': 0.1,
            'help': 'Largura da porta em centímetros'
        }
    ]
    
    @staticmethod
    def calcular(dados, componente, componentes_adicionais=None):
        """
        Calcula a quantidade de material necessária para portas de correr
        
        Args:
            dados (dict): Dicionário com quantidade, altura, largura
            componente (Componente): Componente principal (MDF)
            componentes_adicionais (list): Lista de componentes adicionais (fita, parafusos)
            
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
                
                if codigo_tipo and codigo_tipo in PortaCorrerRule.CALCULADORAS_ADICIONAIS:
                    funcao_calculo = PortaCorrerRule.CALCULADORAS_ADICIONAIS[codigo_tipo]
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
            'resumo': f"{quantidade}x portas de correr de {altura}cm x {largura}cm = {resultado_mdf['quantidade_utilizada']} m²"
        }
