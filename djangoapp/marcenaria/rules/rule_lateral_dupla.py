class LateralDuplaRule:
    """Classe com as regras para calcular Lateral Dupla"""
    
    # Componentes que esta peça pode usar
    COMPONENTES_DISPONIVEIS = ['AC-001']  # MDF
    
    # Campos necessários para o cálculo
    CAMPOS_NECESSARIOS = [
        {
            'name': 'quantidade',
            'label': 'Quantidade de laterais',
            'type': 'number',
            'required': True,
            'min': 1,
            'help': 'Quantas laterais duplas você precisa'
        },
        {
            'name': 'altura',
            'label': 'Altura (cm)',
            'type': 'number',
            'required': True,
            'min': 0.1,
            'step': 0.1,
            'help': 'Altura da lateral em centímetros'
        },
        {
            'name': 'largura',
            'label': 'Largura (cm)',
            'type': 'number',
            'required': True,
            'min': 0.1,
            'step': 0.1,
            'help': 'Largura da lateral em centímetros'
        }
    ]
    
    @staticmethod
    def calcular(dados, componente):
        """
        Calcula a quantidade de material necessária para laterais duplas
        
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
        
        # Lateral dupla = 2x a área de uma lateral simples
        area_por_lateral = altura_m * largura_m * 2
        area_total = area_por_lateral * quantidade
        
        return {
            'sucesso': True,
            'area_por_lateral': area_por_lateral,
            'area_total': area_total,
            'quantidade_utilizada': area_total,
            'unidade': 'm²',
            'resumo': f'{quantidade}x laterais duplas de {altura}cm x {largura}cm = {area_total:.4f} m²'
        }