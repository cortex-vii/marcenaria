"""
Utilitário para gerenciar as regras de cálculo das peças
"""
import importlib
import os


class RuleManager:
    """Gerenciador das regras de cálculo das peças"""
    
    _rules_cache = {}
    
    @classmethod
    def get_rule_class(cls, tipo_peca_codigo):
        """
        A função get_rule_class do RuleManager é responsável por localizar e 
        retornar a classe Python que implementa as regras de cálculo para um determinado tipo de peça.
        """
        if tipo_peca_codigo in cls._rules_cache:
            return cls._rules_cache[tipo_peca_codigo]
        
        # Mapear códigos para nomes de arquivos
        code_to_file = {
            'PC-001': 'rule_base_dupla',
            'PC-002': 'rule_base_simples', 
            'PC-003': 'rule_engrossa',
            'PC-004': 'rule_fundo_simples',
            'PC-005': 'rule_gaveta',
            'PC-006': 'rule_lateral_dupla',
            'PC-007': 'rule_lateral_engrossada',
            'PC-008': 'rule_lateral_externa',
            'PC-009': 'rule_lateral_simples',
            'PC-010': 'rule_porta_abrir',
            'PC-011': 'rule_porta_correr',
            'PC-012': 'rule_roda_forro',
            'PC-013': 'rule_roda_pe',
        }
        
        # Mapear nomes de arquivos para nomes de classes
        file_to_class = {
            'rule_base_dupla': 'BaseDuplaRule',
            'rule_base_simples': 'BaseSimplesRule',
            'rule_engrossa': 'EngrossaRule',
            'rule_fundo_simples': 'FundoSimplesRule',
            'rule_gaveta': 'GavetaRule',
            'rule_lateral_dupla': 'LateralDuplaRule',
            'rule_lateral_engrossada': 'LateralEngrossadaRule',
            'rule_lateral_externa': 'LateralExternaRule',
            'rule_lateral_simples': 'LateralSimplesRule',
            'rule_porta_abrir': 'PortaAbrirRule',
            'rule_porta_correr': 'PortaCorrerRule',
            'rule_roda_forro': 'RodaForroRule',
            'rule_roda_pe': 'RodaPeRule',
        }
        
        file_name = code_to_file.get(tipo_peca_codigo)
        if not file_name:
            cls._rules_cache[tipo_peca_codigo] = None
            return None
        
        class_name = file_to_class.get(file_name)
        if not class_name:
            cls._rules_cache[tipo_peca_codigo] = None
            return None
        
        try:
            # Importar o módulo
            module = importlib.import_module(f'marcenaria.rules.{file_name}')
            rule_class = getattr(module, class_name)
            cls._rules_cache[tipo_peca_codigo] = rule_class
            return rule_class
        except (ImportError, AttributeError) as e:
            print(f"Erro ao carregar regra para {tipo_peca_codigo}: {e}")
            cls._rules_cache[tipo_peca_codigo] = None
            return None
    
    @classmethod
    def get_componentes_disponiveis(cls, tipo_peca_codigo):
        """
        Obtém os componentes disponíveis para um tipo de peça
        
        Args:
            tipo_peca_codigo (str): Código do tipo de peça
            
        Returns:
            list: Lista de códigos de componentes disponíveis
        """
        rule_class = cls.get_rule_class(tipo_peca_codigo)
        if rule_class and hasattr(rule_class, 'COMPONENTES_DISPONIVEIS'):
            return rule_class.COMPONENTES_DISPONIVEIS
        return []
    
    @classmethod
    def get_campos_necessarios(cls, tipo_peca_codigo):
        """
        Obtém os campos necessários para o cálculo de um tipo de peça
        
        Args:
            tipo_peca_codigo (str): Código do tipo de peça
            
        Returns:
            list: Lista de dicionários com informações dos campos
        """
        rule_class = cls.get_rule_class(tipo_peca_codigo)
        if rule_class and hasattr(rule_class, 'CAMPOS_NECESSARIOS'):
            return rule_class.CAMPOS_NECESSARIOS
        return []
    
    @classmethod
    def calcular(cls, tipo_peca_codigo, dados, componente):
        """
        Executa o cálculo para um tipo de peça
        
        Args:
            tipo_peca_codigo (str): Código do tipo de peça
            dados (dict): Dados do formulário
            componente (Componente): Instância do componente selecionado
            
        Returns:
            dict: Resultado do cálculo
        """
        rule_class = cls.get_rule_class(tipo_peca_codigo)
        if rule_class and hasattr(rule_class, 'calcular'):
            return rule_class.calcular(dados, componente)
        return {'erro': 'Regra de cálculo não encontrada'}
    
    @classmethod
    def limpar_cache(cls):
        """Limpa o cache de regras (útil para desenvolvimento)"""
        cls._rules_cache.clear()