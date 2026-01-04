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

def calcular_parafusos_fundo_simples(dados, componente_parafuso):
    """
    Calcula o custo dos parafusos para fundo simples.
    Soma altura + largura, a cada 15cm = 1 parafuso, multiplicado pela quantidade.
    """
    quantidade = float(dados.get('quantidade', 0))
    altura = float(dados.get('altura', 0))
    largura = float(dados.get('largura', 0))
    
    # Validação
    if quantidade <= 0:
        return {
            'erro': 'Quantidade deve ser maior que zero'
        }
    
    # Soma da metragem (em cm)
    soma_metragem = altura + largura
    
    # A cada 15cm = 1 parafuso
    parafusos_por_peca = soma_metragem / 15
    
    # Total de parafusos
    quantidade_parafusos = parafusos_por_peca * quantidade
    
    custo_unitario = float(getattr(componente_parafuso, 'custo_unitario', 0))
    custo_total = quantidade_parafusos * custo_unitario
    
    return {
        'componente': componente_parafuso.nome,
        'quantidade_utilizada': format_decimal(quantidade_parafusos),
        'unidade': 'un',
        'custo_total': format_decimal(custo_total),
        'resumo': f'{format_decimal(quantidade_parafusos)} parafusos para {format_decimal(quantidade)} peças ({format_decimal(parafusos_por_peca)} por peça - 1 a cada 15cm)'
    }

def calcular_parafusos_porta_abrir(dados, componente_parafuso):
    """
    Calcula o custo dos parafusos para portas de abrir.
    Para cada dobradiça, são necessários 4 parafusos.
    A quantidade de dobradiças depende da altura da porta.
    """
    quantidade = float(dados.get('quantidade', 0))
    altura = float(dados.get('altura', 0))  # em cm
    
    # Validação
    if quantidade <= 0:
        return {
            'erro': 'Quantidade deve ser maior que zero'
        }
    
    # Converter altura de cm para metros
    altura_m = altura / 100
    
    # Determinar quantidade de dobradiças por porta baseado na altura
    if altura_m > 2.50:
        dobradicas_por_porta = 5
    elif altura_m > 1.69:
        dobradicas_por_porta = 4
    elif altura_m > 0.90:
        dobradicas_por_porta = 3
    else:
        dobradicas_por_porta = 2
    
    # Total de dobradiças
    quantidade_dobradicas = dobradicas_por_porta * quantidade
    
    # Parafusos: 4 por dobradiça
    quantidade_parafusos = quantidade_dobradicas * 4
    
    custo_unitario = float(getattr(componente_parafuso, 'custo_unitario', 0))
    custo_total = quantidade_parafusos * custo_unitario
    
    return {
        'componente': componente_parafuso.nome,
        'quantidade_utilizada': format_decimal(quantidade_parafusos),
        'unidade': 'un',
        'custo_total': format_decimal(custo_total),
        'resumo': f'{format_decimal(quantidade_parafusos)} parafusos para {format_decimal(quantidade)} portas ({format_decimal(quantidade_dobradicas)} dobradiças x 4 parafusos)'
    }

