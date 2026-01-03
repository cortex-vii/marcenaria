from marcenaria.utils.data_format import format_decimal

def calcular_custo_fita(dados, componente_fita):
    # Exemplo: calcula perímetro * quantidade * preço da fita
    altura = float(dados.get('altura', 0))
    largura = float(dados.get('largura', 0))
    quantidade = float(dados.get('quantidade', 0))
    perimetro = 2 * (altura + largura)
    total_metros = perimetro * quantidade / 100  # se altura/largura em cm
    custo_unitario = float(getattr(componente_fita, 'custo_unitario', 0))
    custo_total = total_metros * custo_unitario
    return {
        'componente': componente_fita.nome,
        'quantidade_utilizada': format_decimal(total_metros),
        'unidade': 'm',
        'custo_total': format_decimal(custo_total),
        'resumo': f'{format_decimal(total_metros)}m de fita para {format_decimal(quantidade)} peças'
    }