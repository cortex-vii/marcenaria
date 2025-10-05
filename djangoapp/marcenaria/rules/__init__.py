"""
Sistema de regras para cálculo de peças
"""

def get_rule_class(codigo_tipo_peca):
    """Retorna a classe de regra para o tipo de peça"""
    
    # Mapeamento de códigos para classes
    RULES_MAP = {
        'PC-004': 'rule_fundo_simples.FundoSimplesRule',  # Fundo simples
    }
    
    if codigo_tipo_peca not in RULES_MAP:
        return None
    
    # Import dinâmico
    module_path, class_name = RULES_MAP[codigo_tipo_peca].split('.')
    
    try:
        module = __import__(f'marcenaria.rules.{module_path}', fromlist=[class_name])
        return getattr(module, class_name)
    except (ImportError, AttributeError):
        return None

def get_campos_para_peca(codigo_tipo_peca):
    """Retorna os campos necessários para uma peça"""
    rule_class = get_rule_class(codigo_tipo_peca)
    if rule_class:
        return rule_class.CAMPOS_NECESSARIOS
    return []

def get_componentes_disponiveis(codigo_tipo_peca):
    """Retorna os componentes disponíveis para uma peça"""
    rule_class = get_rule_class(codigo_tipo_peca)
    if rule_class:
        return rule_class.COMPONENTES_DISPONIVEIS
    return []