from marcenaria.utils.data_format import format_decimal

def calcular_custo_parafusos(dados, componente_parafuso):
    """
    Calcula o custo dos parafusos com base na quantidade de peças.
    Para cada peça, são necessários 6 parafusos.
    """
    quantidade = float(dados.get('quantidade', 0))
    
    # Validação
    if quantidade <= 0:
        return {
            'erro': 'Quantidade deve ser maior que zero'
        }
    
    # Calcular quantidade total de parafusos (6 por peça)
    quantidade_parafusos = quantidade * 6
    
    custo_unitario = float(getattr(componente_parafuso, 'custo_unitario', 0))
    custo_total = quantidade_parafusos * custo_unitario
    
    return {
        'componente': componente_parafuso.nome,
        'quantidade_utilizada': format_decimal(quantidade_parafusos),
        'unidade': 'un',
        'custo_total': format_decimal(custo_total),
        'resumo': f'{format_decimal(quantidade_parafusos)} parafusos para {format_decimal(quantidade)} peças (6 por peça)'
    }
