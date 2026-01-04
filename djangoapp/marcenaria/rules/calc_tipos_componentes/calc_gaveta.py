from marcenaria.utils.data_format import format_decimal

def calcular_custo_mdf_laterais_gaveta(dados, componente_mdf):
    """
    Calcula o custo do MDF para laterais da gaveta.
    Fórmula: altura × profundidade × 2
    """
    quantidade = float(dados.get('quantidade', 0))
    altura = float(dados.get('altura', 0))  # em cm
    profundidade = float(dados.get('profundidade', 0))  # em cm
    
    # Validações
    if quantidade <= 0 or altura <= 0 or profundidade <= 0:
        return {
            'erro': 'Quantidade, altura e profundidade devem ser maiores que zero'
        }
    
    # Converter cm para metros
    altura_m = altura / 100
    profundidade_m = profundidade / 100
    
    # 2 Laterais: altura × profundidade × 2
    area_laterais = altura_m * profundidade_m * 2
    area_total = area_laterais * quantidade
    
    custo_unitario = float(getattr(componente_mdf, 'custo_unitario', 0))
    custo_total = area_total * custo_unitario
    
    return {
        'componente': componente_mdf.nome,
        'quantidade_utilizada': format_decimal(area_total),
        'unidade': 'm²',
        'custo_total': format_decimal(custo_total),
        'resumo': f"{format_decimal(area_total)} m² de MDF para laterais ({format_decimal(altura)}cm altura × {format_decimal(profundidade)}cm profundidade × 2 laterais) - {format_decimal(quantidade)} gavetas"
    }


def calcular_custo_mdf_frente_gaveta(dados, componente_mdf):
    """
    Calcula o custo do MDF para frente da gaveta.
    Fórmula: altura × largura
    """
    quantidade = float(dados.get('quantidade', 0))
    altura = float(dados.get('altura', 0))  # em cm
    largura = float(dados.get('largura', 0))  # em cm
    
    # Validações
    if quantidade <= 0 or altura <= 0 or largura <= 0:
        return {
            'erro': 'Quantidade, altura e largura devem ser maiores que zero'
        }
    
    # Converter cm para metros
    altura_m = altura / 100
    largura_m = largura / 100
    
    # Frente: altura × largura
    area_frente = altura_m * largura_m
    area_total = area_frente * quantidade
    
    custo_unitario = float(getattr(componente_mdf, 'custo_unitario', 0))
    custo_total = area_total * custo_unitario
    
    return {
        'componente': componente_mdf.nome,
        'quantidade_utilizada': format_decimal(area_total),
        'unidade': 'm²',
        'custo_total': format_decimal(custo_total),
        'resumo': f"{format_decimal(area_total)} m² de MDF para frente ({format_decimal(altura)}cm altura × {format_decimal(largura)}cm largura) - {format_decimal(quantidade)} gavetas"
    }


def calcular_custo_mdf_fundo_traseiro_gaveta(dados, componente_mdf):
    """
    Calcula o custo do MDF para fundo traseiro da gaveta.
    Fórmula: altura × largura
    """
    quantidade = float(dados.get('quantidade', 0))
    altura = float(dados.get('altura', 0))  # em cm
    largura = float(dados.get('largura', 0))  # em cm
    
    # Validações
    if quantidade <= 0 or altura <= 0 or largura <= 0:
        return {
            'erro': 'Quantidade, altura e largura devem ser maiores que zero'
        }
    
    # Converter cm para metros
    altura_m = altura / 100
    largura_m = largura / 100
    
    # Fundo traseiro: altura × largura
    area_fundo = altura_m * largura_m
    area_total = area_fundo * quantidade
    
    custo_unitario = float(getattr(componente_mdf, 'custo_unitario', 0))
    custo_total = area_total * custo_unitario
    
    return {
        'componente': componente_mdf.nome,
        'quantidade_utilizada': format_decimal(area_total),
        'unidade': 'm²',
        'custo_total': format_decimal(custo_total),
        'resumo': f"{format_decimal(area_total)} m² de MDF para fundo traseiro ({format_decimal(altura)}cm altura × {format_decimal(largura)}cm largura) - {format_decimal(quantidade)} gavetas"
    }


def calcular_custo_fundo_gaveta(dados, componente_fundo):
    """
    Calcula o custo do fundo da gaveta (chapa de fundo).
    Fórmula: largura × profundidade × quantidade
    """
    quantidade = float(dados.get('quantidade', 0))
    largura = float(dados.get('largura', 0))  # em cm
    profundidade = float(dados.get('profundidade', 0))  # em cm
    
    # Validações
    if quantidade <= 0 or largura <= 0 or profundidade <= 0:
        return {
            'erro': 'Quantidade, largura e profundidade devem ser maiores que zero'
        }
    
    # Converter cm para metros
    largura_m = largura / 100
    profundidade_m = profundidade / 100
    
    # Área do fundo por gaveta
    area_por_fundo = largura_m * profundidade_m
    
    # Área total
    area_total = area_por_fundo * quantidade
    
    custo_unitario = float(getattr(componente_fundo, 'custo_unitario', 0))
    custo_total = area_total * custo_unitario
    
    return {
        'componente': componente_fundo.nome,
        'quantidade_utilizada': format_decimal(area_total),
        'unidade': 'm²',
        'custo_total': format_decimal(custo_total),
        'resumo': f"{format_decimal(area_total)} m² de fundo/chapa ({format_decimal(largura)}cm largura × {format_decimal(profundidade)}cm profundidade) - {format_decimal(quantidade)} gavetas"
    }


def calcular_custo_fita_gaveta(dados, componente_fita):
    """
    Calcula o custo da fita para gaveta (perímetro do topo).
    Fórmula: 2 × (largura + profundidade) × quantidade
    """
    quantidade = float(dados.get('quantidade', 0))
    largura = float(dados.get('largura', 0))  # em cm
    profundidade = float(dados.get('profundidade', 0))  # em cm
    
    # Validação
    if quantidade <= 0 or largura <= 0 or profundidade <= 0:
        return {
            'erro': 'Quantidade, largura e profundidade devem ser maiores que zero'
        }
    
    # Converter cm para metros
    largura_m = largura / 100
    profundidade_m = profundidade / 100
    
    # Perímetro do topo da gaveta
    perimetro_por_gaveta = 2 * (largura_m + profundidade_m)
    
    # Total de metros
    total_metros = perimetro_por_gaveta * quantidade
    
    custo_unitario = float(getattr(componente_fita, 'custo_unitario', 0))
    custo_total = total_metros * custo_unitario
    
    return {
        'componente': componente_fita.nome,
        'quantidade_utilizada': format_decimal(total_metros),
        'unidade': 'm',
        'custo_total': format_decimal(custo_total),
        'resumo': f'{format_decimal(total_metros)}m de fita para {format_decimal(quantidade)} gavetas'
    }


def calcular_custo_corredicas_gaveta(dados, componente_corredica):
    """
    Calcula o custo das corrediças para gaveta.
    Fórmula: 1 par por gaveta
    """
    quantidade = float(dados.get('quantidade', 0))
    
    # Validação
    if quantidade <= 0:
        return {
            'erro': 'Quantidade deve ser maior que zero'
        }
    
    # 1 par por gaveta
    pares_necessarios = quantidade
    
    custo_unitario = float(getattr(componente_corredica, 'custo_unitario', 0))
    custo_total = pares_necessarios * custo_unitario
    
    return {
        'componente': componente_corredica.nome,
        'quantidade_utilizada': format_decimal(pares_necessarios),
        'unidade': 'pares',
        'custo_total': format_decimal(custo_total),
        'resumo': f'{format_decimal(pares_necessarios)} pares de corrediças para {format_decimal(quantidade)} gavetas'
    }


def calcular_parafusos_gaveta(dados, componente_parafuso):
    """
    Calcula o custo dos parafusos para gaveta.
    Fórmula: 20 parafusos por gaveta
    """
    quantidade = float(dados.get('quantidade', 0))
    
    # Validação
    if quantidade <= 0:
        return {
            'erro': 'Quantidade deve ser maior que zero'
        }
    
    # 20 parafusos por gaveta
    quantidade_parafusos = 20 * quantidade
    
    custo_unitario = float(getattr(componente_parafuso, 'custo_unitario', 0))
    custo_total = quantidade_parafusos * custo_unitario
    
    return {
        'componente': componente_parafuso.nome,
        'quantidade_utilizada': format_decimal(quantidade_parafusos),
        'unidade': 'un',
        'custo_total': format_decimal(custo_total),
        'resumo': f'{format_decimal(quantidade_parafusos)} parafusos para {format_decimal(quantidade)} gavetas (20 por gaveta)'
    }
