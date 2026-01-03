from marcenaria.utils.data_format import format_decimal

def calcular_custo_mdf(dados, componente_mdf):
    """
    Calcula o custo do MDF com base nos dados da peça e no componente MDF fornecido.
    Espera que os dados contenham 'quantidade', 'altura' e 'largura' em centímetros.
    O componente deve ter o atributo 'custo_unitario' (preço por m²).
    """
    quantidade = float(dados.get('quantidade', 0))
    altura = float(dados.get('altura', 0))
    largura = float(dados.get('largura', 0))

    # Validações
    if quantidade <= 0 or altura <= 0 or largura <= 0:
        return {
            'erro': 'Quantidade, altura e largura devem ser maiores que zero'
        }

    # Converter cm para metros
    altura_m = altura / 100
    largura_m = largura / 100

    # Calcular área por peça e total
    area_por_peca = altura_m * largura_m
    area_total = area_por_peca * quantidade

    custo_unitario = float(getattr(componente_mdf, 'custo_unitario', 0))
    custo_total = area_total * custo_unitario

    return {
        'componente': componente_mdf.nome,
        'quantidade_utilizada': format_decimal(area_total),
        'unidade': 'm²',
        'custo_total': format_decimal(custo_total),
        'resumo': f"{format_decimal(area_total)} m² de MDF para {format_decimal(quantidade)} peças"
    }
