class RodaPeRule:
    """Classe com as regras para calcular Roda Pé"""
    
    # Componentes que esta peça pode usar
    COMPONENTES_DISPONIVEIS = ['AC-001', 'AC-002']  # MDF e FITA
    
    # Campos necessários para o cálculo
    CAMPOS_NECESSARIOS = [
        {
            'name': 'quantidade',
            'label': 'Quantidade de rodas pé',
            'type': 'number',
            'required': True,
            'min': 1,
            'help': 'Quantas rodas pé você precisa'
        },
        {
            'name': 'altura',
            'label': 'Altura (cm)',
            'type': 'number',
            'required': True,
            'min': 0.1,
            'step': 0.1,
            'help': 'Altura da roda pé em centímetros'
        },
        {
            'name': 'largura',
            'label': 'Largura (cm)',
            'type': 'number',
            'required': True,
            'min': 0.1,
            'step': 0.1,
            'help': 'Largura da roda pé em centímetros'
        }
    ]
    
    @staticmethod
    def calcular(dados, componente):
        """
        Calcula a quantidade de material necessária para rodas pé
        
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
            # Calcular área para MDF
            area_por_roda = altura_m * largura_m
            area_total = area_por_roda * quantidade
            
            return {
                'sucesso': True,
                'area_por_roda': area_por_roda,
                'area_total': area_total,
                'quantidade_utilizada': area_total,
                'unidade': 'm²',
                'resumo': f'{quantidade}x rodas pé de {altura}cm x {largura}cm = {area_total:.4f} m²'
            }
        
        elif componente.tipo_componente.codigo == 'AC-002':  # FITA
            # Calcular perímetro para fitas de borda
            perimetro_por_roda = 2 * (altura_m + largura_m)
            perimetro_total = perimetro_por_roda * quantidade
            
            return {
                'sucesso': True,
                'perimetro_por_roda': perimetro_por_roda,
                'perimetro_total': perimetro_total,
                'quantidade_utilizada': perimetro_total,
                'unidade': 'm',
                'resumo': f'{quantidade}x rodas pé = {perimetro_total:.2f}m de fita'
            }
        
        else:
            return {'erro': 'Componente não compatível com rodas pé'}