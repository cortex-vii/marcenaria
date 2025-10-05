class BaseEngrossadaRule:
    """Classe com as regras para calcular Base Engrossada"""
    
    # Componentes que esta peça pode usar
    COMPONENTES_DISPONIVEIS = ['AC-001']  # MDF
    
    # Campos necessários para o cálculo
    CAMPOS_NECESSARIOS = [
        {
            'name': 'quantidade',
            'label': 'Quantidade de peças',
            'type': 'number',
            'required': True,
            'min': 1,
            'help': 'Quantas peças de base engrossada você precisa'
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
            'name': 'espessura_extra',
            'label': 'Espessura extra (cm)',
            'type': 'number',
            'required': True,
            'min': 0.1,
            'step': 0.1,
            'help': 'Espessura adicional para o engrossamento'
        }
    ]
    
    @staticmethod
    def calcular(dados, componente):
        """
        Calcula a quantidade de material necessária para base engrossada
        
        Args:
            dados (dict): Dicionário com quantidade, altura, largura, espessura_extra
            componente (Componente): Componente selecionado
            
        Returns:
            dict: Resultado do cálculo
        """
        quantidade = float(dados.get('quantidade', 0))
        altura = float(dados.get('altura', 0))
        largura = float(dados.get('largura', 0))
        espessura_extra = float(dados.get('espessura_extra', 0))
        
        # Validações
        if quantidade <= 0:
            return {'erro': 'Quantidade deve ser maior que zero'}
        if altura <= 0:
            return {'erro': 'Altura deve ser maior que zero'}
        if largura <= 0:
            return {'erro': 'Largura deve ser maior que zero'}
        if espessura_extra <= 0:
            return {'erro': 'Espessura extra deve ser maior que zero'}
        
        # Converter cm para metros
        altura_m = altura / 100
        largura_m = largura / 100
        espessura_extra_m = espessura_extra / 100
        
        # Base engrossada = área base + área das bordas de engrossamento
        area_base = altura_m * largura_m
        # Bordas: 2 * (altura + largura) * espessura_extra
        area_bordas = 2 * (altura_m + largura_m) * espessura_extra_m
        area_por_peca = area_base + area_bordas
        area_total = area_por_peca * quantidade
        
        return {
            'sucesso': True,
            'area_base': area_base,
            'area_bordas': area_bordas,
            'area_por_peca': area_por_peca,
            'area_total': area_total,
            'quantidade_utilizada': area_total,
            'unidade': 'm²',
            'resumo': f'{quantidade}x bases engrossadas de {altura}cm x {largura}cm (+{espessura_extra}cm) = {area_total:.4f} m²'
        }