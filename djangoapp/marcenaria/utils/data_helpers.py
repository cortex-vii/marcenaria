"""
Utilitários para facilitar o acesso aos dados por código
"""
from marcenaria.models import TipoPeca, TipoComponente, Fornecedor

class DataHelper:
    """Classe para facilitar busca de dados por código"""
    
    @staticmethod
    def get_tipo_peca_by_codigo(codigo):
        """Busca tipo de peça por código"""
        try:
            return TipoPeca.objects.get(codigo=codigo)
        except TipoPeca.DoesNotExist:
            return None
    
    @staticmethod
    def get_tipo_componente_by_codigo(codigo):
        """Busca tipo de componente por código"""
        try:
            return TipoComponente.objects.get(codigo=codigo)
        except TipoComponente.DoesNotExist:
            return None
    
    @staticmethod
    def get_fornecedor_by_codigo(codigo):
        """Busca fornecedor por código"""
        try:
            return Fornecedor.objects.get(codigo=codigo)
        except Fornecedor.DoesNotExist:
            return None

# Exemplo de uso:
# mdf = DataHelper.get_tipo_componente_by_codigo('AC-001')
# base_dupla = DataHelper.get_tipo_peca_by_codigo('PC-001')
# fornecedor = DataHelper.get_fornecedor_by_codigo('FOR-001')