class GavetaRule:
    """Classe com as regras para calcular Gaveta"""
    
    # Componentes que esta peça pode usar
    COMPONENTES_DISPONIVEIS = ['AC-001', 'AC-004']  # MDF e CORREDIÇAS
    
    # Campos necessários para o cálculo
    CAMPOS_NECESSARIOS = [
        {
            'name': 'quantidade',
            'label': 'Quantidade de gavetas',
            'type': 'number',
            'required': True,
            'min': 1,
            'help': 'Quantas gavetas você precisa'
        },
        {
            'name': 'altura',
            'label': 'Altura (cm)',
            'type': 'number',
            'required': True,
            'min': 0.1,
            'step': 0.1,
            'help': 'Altura da gaveta em centímetros'
        },
        {
            'name': 'largura',
            'label': 'Largura (cm)',
            'type': 'number',
            'required': True,
            'min': 0.1,
            'step': 0.1,
            'help': 'Largura da gaveta em centímetros'
        },
        {
            'name': 'profundidade',
            'label': 'Profundidade (cm)',
            'type': 'number',
            'required': True,
            'min': 0.1,
            'step': 0.1,
            'help': 'Profundidade da gaveta em centímetros'
        }
    ]
    
    @staticmethod
    def calcular(dados, componente):
        """
        Calcula a quantidade de material necessária para gavetas
        
        Args:
            dados (dict): Dicionário com quantidade, altura, largura, profundidade
            componente (Componente): Componente selecionado
            
        Returns:
            dict: Resultado do cálculo
        """
        quantidade = float(dados.get('quantidade', 0))
        altura = float(dados.get('altura', 0))
        largura = float(dados.get('largura', 0))
        profundidade = float(dados.get('profundidade', 0))
        
        # Validações
        if quantidade <= 0:
            return {'erro': 'Quantidade deve ser maior que zero'}
        if altura <= 0:
            return {'erro': 'Altura deve ser maior que zero'}
        if largura <= 0:
            return {'erro': 'Largura deve ser maior que zero'}
        if profundidade <= 0:
            return {'erro': 'Profundidade deve ser maior que zero'}
        
        # Converter cm para metros
        altura_m = altura / 100
        largura_m = largura / 100
        profundidade_m = profundidade / 100
        
        if componente.tipo_componente.codigo == 'AC-001':  # MDF
            # Para MDF: calcular área das peças (fundo + laterais + frente/fundo)
            # Fundo: largura x profundidade
            # 2 Laterais: altura x profundidade
            # Frente e fundo: altura x largura
            area_fundo = largura_m * profundidade_m
            area_laterais = 2 * (altura_m * profundidade_m)
            area_frente_fundo = 2 * (altura_m * largura_m)
            area_por_gaveta = area_fundo + area_laterais + area_frente_fundo
            area_total = area_por_gaveta * quantidade
            
            return {
                'sucesso': True,
                'area_por_gaveta': area_por_gaveta,
                'area_total': area_total,
                'quantidade_utilizada': area_total,
                'unidade': 'm²',
                'resumo': f'{quantidade}x gavetas de {altura}cm x {largura}cm x {profundidade}cm = {area_total:.4f} m²'
            }
        
        elif componente.tipo_componente.codigo == 'AC-004':  # CORREDIÇAS
            # Para corrediças: 1 par por gaveta
            pares_necessarios = quantidade
            
            return {
                'sucesso': True,
                'pares_por_gaveta': 1,
                'pares_total': pares_necessarios,
                'quantidade_utilizada': pares_necessarios,
                'unidade': 'pares',
                'resumo': f'{quantidade}x gavetas = {pares_necessarios} pares de corrediças'
            }
        
        else:
            return {'erro': 'Componente não compatível com gavetas'}