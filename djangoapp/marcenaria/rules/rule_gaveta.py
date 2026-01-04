from .calc_tipos_componentes.calc_gaveta import (
    calcular_custo_mdf_laterais_gaveta,
    calcular_custo_mdf_frente_gaveta,
    calcular_custo_mdf_fundo_traseiro_gaveta,
    calcular_custo_fundo_gaveta,
    calcular_custo_fita_gaveta,
    calcular_custo_corredicas_gaveta,
    calcular_parafusos_gaveta
)
from ..utils.data_format import format_decimal

class GavetaRule:
    """Classe com as regras para calcular Gaveta"""
    
    # Componentes que esta peça pode usar
    # Gaveta usa 4 MDFs separados que serão solicitados como componentes adicionais
    COMPONENTES_DISPONIVEIS = ['AC-001']  # Primeiro MDF - Laterais da gaveta
    COMPONENTES_ADICIONAIS = [
        'AC-001',  # MDF Frente da gaveta
        'AC-001',  # MDF Fundo traseiro da gaveta
        'AC-001',  # MDF Fundo da gaveta (chapa)
        'AC-002',  # Fita de borda
        'AC-004',  # Corrediças
        'AC-006'   # Parafusos
    ]
    
    # Configuração de componentes MDF com campos específicos para cada um
    COMPONENTES_MDF_CONFIG = [
        {
            'label': 'MDF - LATERAIS DA GAVETA',
            'codigo': 'AC-001',
            'calculadora': calcular_custo_mdf_laterais_gaveta,
            'campos': [
                {'name': 'altura_laterais', 'label': 'Altura das Laterais (cm)', 'type': 'number', 'required': True, 'min': 0.1, 'step': 0.1},
                {'name': 'profundidade_laterais', 'label': 'Profundidade das Laterais (cm)', 'type': 'number', 'required': True, 'min': 0.1, 'step': 0.1}
            ]
        },
        {
            'label': 'MDF - FRENTE DA GAVETA',
            'codigo': 'AC-001',
            'calculadora': calcular_custo_mdf_frente_gaveta,
            'campos': [
                {'name': 'altura_frente', 'label': 'Altura da Frente (cm)', 'type': 'number', 'required': True, 'min': 0.1, 'step': 0.1},
                {'name': 'largura_frente', 'label': 'Largura da Frente (cm)', 'type': 'number', 'required': True, 'min': 0.1, 'step': 0.1}
            ]
        },
        {
            'label': 'MDF - FUNDO TRASEIRO DA GAVETA',
            'codigo': 'AC-001',
            'calculadora': calcular_custo_mdf_fundo_traseiro_gaveta,
            'campos': [
                {'name': 'altura_fundo_traseiro', 'label': 'Altura do Fundo Traseiro (cm)', 'type': 'number', 'required': True, 'min': 0.1, 'step': 0.1},
                {'name': 'largura_fundo_traseiro', 'label': 'Largura do Fundo Traseiro (cm)', 'type': 'number', 'required': True, 'min': 0.1, 'step': 0.1}
            ]
        },
        {
            'label': 'MDF - FUNDO DA GAVETA (CHAPA)',
            'codigo': 'AC-001',
            'calculadora': calcular_custo_fundo_gaveta,
            'campos': [
                {'name': 'largura_fundo', 'label': 'Largura do Fundo (cm)', 'type': 'number', 'required': True, 'min': 0.1, 'step': 0.1},
                {'name': 'profundidade_fundo', 'label': 'Profundidade do Fundo (cm)', 'type': 'number', 'required': True, 'min': 0.1, 'step': 0.1}
            ]
        }
    ]
    
    # Mapeamento de códigos de tipo de componente para funções de cálculo (não-MDF)
    CALCULADORAS_ADICIONAIS = {
        'AC-002': calcular_custo_fita_gaveta,        # Fita de borda
        'AC-004': calcular_custo_corredicas_gaveta,  # Corrediças
        'AC-006': calcular_parafusos_gaveta,         # Parafusos (20 por gaveta)
    }
    
    # Campos necessários para o cálculo (apenas quantidade, os demais são por componente)
    CAMPOS_NECESSARIOS = [
        {
            'name': 'quantidade',
            'label': 'Quantidade de gavetas',
            'type': 'number',
            'required': True,
            'min': 1,
            'help': 'Quantas gavetas você precisa'
        }
    ]
    
    @staticmethod
    def calcular(dados, componente, componentes_adicionais=None):
        """
        Calcula a quantidade de material necessária para gavetas
        
        Args:
            dados (dict): Dicionário com quantidade, altura, largura, profundidade
            componente: Componente MDF principal (laterais da gaveta)
            componentes_adicionais (list): Lista de componentes adicionais incluindo:
                - 3 MDFs adicionais (frente, fundo traseiro, fundo chapa)
                - Fita, corrediças, parafusos
            
        Returns:
            dict: Resultado do cálculo
        """
        def parse_float(val):
            if isinstance(val, str):
                return float(val.replace(',', '.'))
            return float(val)

        quantidade = float(dados.get('quantidade', 0))

        # Processar todos os componentes MDF usando a configuração
        custo_total = 0
        area_total = 0
        detalhes = []
        
        # Mapear dados de entrada para cada tipo de MDF
        dados_por_tipo = {
            'laterais': {
                'quantidade': quantidade,
                'altura': float(dados.get('altura_laterais', 0)),
                'profundidade': float(dados.get('profundidade_laterais', 0))
            },
            'frente': {
                'quantidade': quantidade,
                'altura': float(dados.get('altura_frente', 0)),
                'largura': float(dados.get('largura_frente', 0))
            },
            'fundo_traseiro': {
                'quantidade': quantidade,
                'altura': float(dados.get('altura_fundo_traseiro', 0)),
                'largura': float(dados.get('largura_fundo_traseiro', 0))
            },
            'fundo': {
                'quantidade': quantidade,
                'largura': float(dados.get('largura_fundo', 0)),
                'profundidade': float(dados.get('profundidade_fundo', 0))
            }
        }
        
        # Processar componente principal (laterais) e adicionais (MDFs)
        componentes_mdf = [componente] + ([comp for comp in (componentes_adicionais or []) 
                                            if hasattr(comp, 'tipo_componente') and comp.tipo_componente.codigo == 'AC-001'][:3])
        
        tipos_mdf = ['laterais', 'frente', 'fundo_traseiro', 'fundo']
        
        for idx, comp_mdf in enumerate(componentes_mdf):
            if idx < len(GavetaRule.COMPONENTES_MDF_CONFIG):
                config = GavetaRule.COMPONENTES_MDF_CONFIG[idx]
                tipo = tipos_mdf[idx]
                
                funcao_calculo = config['calculadora']
                dados_calculo = dados_por_tipo[tipo]
                
                resultado = funcao_calculo(dados_calculo, comp_mdf)
                
                if resultado.get('erro'):
                    return {'erro': f"{config['label']}: {resultado['erro']}"}
                
                custo_total += parse_float(resultado['custo_total'])
                area_total += parse_float(resultado['quantidade_utilizada'])
                
                detalhes.append({
                    'componente': comp_mdf.nome,
                    'tipo': tipo,
                    'quantidade': resultado['quantidade_utilizada'],
                    'unidade': resultado.get('unidade', 'm²'),
                    'custo': resultado['custo_total'],
                    'resumo': resultado['resumo']
                })
        
        # Processar componentes adicionais não-MDF (fita, corrediças, parafusos)
        if componentes_adicionais:
            for comp in componentes_adicionais:
                codigo_tipo = comp.tipo_componente.codigo if hasattr(comp, 'tipo_componente') else None
                
                if codigo_tipo and codigo_tipo in GavetaRule.CALCULADORAS_ADICIONAIS:
                    funcao_calculo = GavetaRule.CALCULADORAS_ADICIONAIS[codigo_tipo]
                    # Usar dados agregados para componentes não-MDF
                    dados_agregados = {
                        'quantidade': quantidade,
                        'altura': dados.get('altura_frente', 0),  # Usar altura da frente
                        'largura': dados.get('largura_frente', 0),  # Usar largura da frente
                        'profundidade': dados.get('profundidade_laterais', 0)  # Usar profundidade das laterais
                    }
                    resultado = funcao_calculo(dados_agregados, comp)
                    
                    if not resultado.get('erro'):
                        custo_total += parse_float(resultado['custo_total'])
                        detalhes.append(resultado)
                    else:
                        print(f"Erro ao calcular {comp.nome}: {resultado.get('erro')}")

        return {
            'sucesso': True,
            'area_por_peca': area_total / quantidade if quantidade > 0 else 0,
            'area_total': area_total,
            'quantidade_utilizada': format_decimal(area_total),
            'unidade': 'm²',
            'custo_total': f"{custo_total:.2f}",
            'detalhes': detalhes,
            'resumo': f"{quantidade}x gavetas = {format_decimal(area_total)} m² total"
        }