from decimal import Decimal
from .base_rule import BaseRule

class BaseDuplaRule(BaseRule):
    """Regra para cálculo de Base Dupla"""
    
    def calcular_area_mdf(self):
        """
        Base dupla: largura x altura x 2 x quantidade
        """
        return self.largura_m * self.altura_m * Decimal('2') * self.quantidade
    
    def calcular_metragem_fita(self):
        """
        Fita: altura x quantidade (apenas nas bordas verticais)
        """
        return self.altura_m * self.quantidade