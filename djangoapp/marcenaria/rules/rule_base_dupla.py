class BaseDuplaRule:
    """Classe com as regras para calcular Base Dupla"""
    
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
            'help': 'Quantas peças de base dupla você precisa'
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
        }
    ]
    
    @staticmethod
    def calcular(dados, componente):
        """
        Calcula a quantidade de material necessária para base dupla
        
        Args:
            dados (dict): Dicionário com quantidade, altura, largura
            componente (Componente): Componente selecionado
            
        Returns:
            dict: Resultado do cálculo
        """
        quantidade = float(dados.get('quantidade', 0))
        altura = float(dados.get('altura', 0))
        largura = float(dados.get('largura', 0))
        
        # Validações
        if quantidade <= 0:
            return {'erro': 'Quantidade deve ser maior que zero'}
        if altura <= 0:
            return {'erro': 'Altura deve ser maior que zero'}
        if largura <= 0:
            return {'erro': 'Largura deve ser maior que zero'}
        
        # Converter cm para metros
        altura_m = altura / 100
        largura_m = largura / 100
        
        # Base dupla = 2x a área de uma base simples
        area_por_peca = altura_m * largura_m * 2
        area_total = area_por_peca * quantidade
        
        # Verificar se o componente tem área suficiente (se for chapa)
        area_componente = 0
        if componente.unidade_medida == 'QUADRADO':
            area_componente = float(componente.altura * componente.largura)
        
        # Calcular quantas chapas são necessárias
        chapas_necessarias = 0
        if area_componente > 0:
            chapas_necessarias = round(area_total / area_componente + 0.5)  # Arredonda para cima
        
        return {
            'sucesso': True,
            'area_por_peca': area_por_peca,
            'area_total': area_total,
            'chapas_necessarias': chapas_necessarias,
            'quantidade_utilizada': area_total,
            'unidade': 'm²',
            'resumo': f'{quantidade}x peças duplas de {altura}cm x {largura}cm = {area_total:.4f} m²'
        }