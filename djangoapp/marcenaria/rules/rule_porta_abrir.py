class PortaAbrirRule:
    """Classe com as regras para calcular Porta de Abrir"""
    
    # Componentes que esta peça pode usar
    COMPONENTES_DISPONIVEIS = ['AC-001', 'AC-005']  # MDF e DOBRADIÇA
    
    # Campos necessários para o cálculo
    CAMPOS_NECESSARIOS = [
        {
            'name': 'quantidade',
            'label': 'Quantidade de portas',
            'type': 'number',
            'required': True,
            'min': 1,
            'help': 'Quantas portas de abrir você precisa'
        },
        {
            'name': 'altura',
            'label': 'Altura (cm)',
            'type': 'number',
            'required': True,
            'min': 0.1,
            'step': 0.1,
            'help': 'Altura da porta em centímetros'
        },
        {
            'name': 'largura',
            'label': 'Largura (cm)',
            'type': 'number',
            'required': True,
            'min': 0.1,
            'step': 0.1,
            'help': 'Largura da porta em centímetros'
        }
    ]
    
    @staticmethod
    def calcular(dados, componente):
        """
        Calcula a quantidade de material necessária para portas de abrir
        
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
        
        if componente.tipo_componente.codigo == 'AC-001':  # MDF
            # Para MDF: calcular área das portas
            area_por_porta = altura_m * largura_m
            area_total = area_por_porta * quantidade
            
            return {
                'sucesso': True,
                'area_por_porta': area_por_porta,
                'area_total': area_total,
                'quantidade_utilizada': area_total,
                'unidade': 'm²',
                'resumo': f'{quantidade}x portas de {altura}cm x {largura}cm = {area_total:.4f} m²'
            }
        
        elif componente.tipo_componente.codigo == 'AC-005':  # DOBRADIÇA
            # Para dobradiças: 2 ou 3 dobradiças por porta dependendo da altura
            dobradicas_por_porta = 2 if altura <= 100 else 3
            dobradicas_total = dobradicas_por_porta * quantidade
            
            return {
                'sucesso': True,
                'dobradicas_por_porta': dobradicas_por_porta,
                'dobradicas_total': dobradicas_total,
                'quantidade_utilizada': dobradicas_total,
                'unidade': 'unidades',
                'resumo': f'{quantidade}x portas = {dobradicas_total} dobradiças ({dobradicas_por_porta} por porta)'
            }
        
        else:
            return {'erro': 'Componente não compatível com portas de abrir'}