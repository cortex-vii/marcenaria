from marcenaria.utils.data_format import format_decimal

def calcular_custo_mdf_roda(dados, componente_mdf):
    """
    Calcula o custo do MDF para roda forro/pé.
    Fórmula: Quantidade × Altura × Largura × 2 + Quantidade × Altura × Profundidade × (1 a cada 50 cm)
    """
    quantidade = float(dados.get('quantidade', 0))
    altura = float(dados.get('altura', 0))  # em cm
    largura = float(dados.get('largura', 0))  # em cm
    profundidade = float(dados.get('profundidade', 0))  # em cm
    
    # Validações
    if quantidade <= 0 or altura <= 0 or largura <= 0 or profundidade <= 0:
        return {
            'erro': 'Quantidade, altura, largura e profundidade devem ser maiores que zero'
        }
    
    # Converter cm para metros
    altura_m = altura / 100
    largura_m = largura / 100
    profundidade_m = profundidade / 100
    
    # Primeira parte: Quantidade × Altura × Largura × 2
    area_parte1 = quantidade * altura_m * largura_m * 2
    
    # Segunda parte: Quantidade × Altura × Profundidade × (1 a cada 50 cm de profundidade)
    unidades_50cm = profundidade / 50
    area_parte2 = quantidade * altura_m * profundidade_m * unidades_50cm
    
    # Área total
    area_total = area_parte1 + area_parte2
    
    custo_unitario = float(getattr(componente_mdf, 'custo_unitario', 0))
    custo_total = area_total * custo_unitario
    
    return {
        'componente': componente_mdf.nome,
        'quantidade_utilizada': format_decimal(area_total),
        'unidade': 'm²',
        'custo_total': format_decimal(custo_total),
        'resumo': f"{format_decimal(area_total)} m² de MDF para {format_decimal(quantidade)} peças"
    }


def calcular_custo_fita_roda(dados, componente_fita):
    """
    Calcula o custo da fita para roda forro/pé.
    Fórmula: Altura × 4 × Quantidade
    """
    quantidade = float(dados.get('quantidade', 0))
    altura = float(dados.get('altura', 0))  # em cm
    
    # Validação
    if quantidade <= 0 or altura <= 0:
        return {
            'erro': 'Quantidade e altura devem ser maiores que zero'
        }
    
    # Converter altura de cm para metros
    altura_m = altura / 100
    
    # Cálculo: altura × 4 × quantidade
    total_metros = altura_m * 4 * quantidade
    
    custo_unitario = float(getattr(componente_fita, 'custo_unitario', 0))
    custo_total = total_metros * custo_unitario
    
    return {
        'componente': componente_fita.nome,
        'quantidade_utilizada': format_decimal(total_metros),
        'unidade': 'm',
        'custo_total': format_decimal(custo_total),
        'resumo': f'{format_decimal(total_metros)}m de fita para {format_decimal(quantidade)} peças'
    }


def calcular_parafusos_roda(dados, componente_parafuso):
    """
    Calcula o custo dos parafusos para roda forro/pé.
    Fórmula: 4 parafusos a cada 50 cm de profundidade × Quantidade
    """
    quantidade = float(dados.get('quantidade', 0))
    profundidade = float(dados.get('profundidade', 0))  # em cm
    
    # Validação
    if quantidade <= 0 or profundidade <= 0:
        return {
            'erro': 'Quantidade e profundidade devem ser maiores que zero'
        }
    
    # 4 parafusos a cada 50 cm
    unidades_50cm = profundidade / 50
    parafusos_por_peca = 4 * unidades_50cm
    
    # Total de parafusos
    quantidade_parafusos = parafusos_por_peca * quantidade
    
    custo_unitario = float(getattr(componente_parafuso, 'custo_unitario', 0))
    custo_total = quantidade_parafusos * custo_unitario
    
    return {
        'componente': componente_parafuso.nome,
        'quantidade_utilizada': format_decimal(quantidade_parafusos),
        'unidade': 'un',
        'custo_total': format_decimal(custo_total),
        'resumo': f'{format_decimal(quantidade_parafusos)} parafusos para {format_decimal(quantidade)} peças ({format_decimal(parafusos_por_peca)} por peça - 4 a cada 50cm)'
    }
