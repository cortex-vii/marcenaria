from marcenaria.utils.data_format import format_decimal

def calcular_custo_dobradicas_porta_abrir(dados, componente_dobradica):
    """
    Calcula o custo das dobradiças para portas de abrir.
    Lógica:
    - Altura > 2,50m = 5 dobradiças por porta
    - Altura > 1,69m = 4 dobradiças por porta
    - Altura > 0,90m = 3 dobradiças por porta
    - Altura <= 0,90m = 2 dobradiças por porta
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
    
    custo_unitario = float(getattr(componente_dobradica, 'custo_unitario', 0))
    custo_total = quantidade_dobradicas * custo_unitario
    
    return {
        'componente': componente_dobradica.nome,
        'quantidade_utilizada': format_decimal(quantidade_dobradicas),
        'unidade': 'un',
        'custo_total': format_decimal(custo_total),
        'resumo': f'{format_decimal(quantidade_dobradicas)} dobradiças para {format_decimal(quantidade)} portas ({dobradicas_por_porta} por porta de {format_decimal(altura_m)}m)'
    }
