from decimal import Decimal
from abc import ABC, abstractmethod

class BaseRule(ABC):
    """Classe base abstrata para regras de cálculo de componentes"""
    
    def __init__(self, largura, altura, quantidade):
        """
        Args:
            largura: Largura em centímetros
            altura: Altura em centímetros
            quantidade: Quantidade de peças
        """
        self.largura = Decimal(str(largura))
        self.altura = Decimal(str(altura))
        self.quantidade = int(quantidade)
        
        # Converter para metros
        self.largura_m = self.largura / Decimal('100')
        self.altura_m = self.altura / Decimal('100')
    
    @abstractmethod
    def calcular_area_mdf(self):
        """Calcula a área de MDF necessária em m²"""
        pass
    
    @abstractmethod
    def calcular_metragem_fita(self):
        """Calcula a metragem de fita necessária em metros"""
        pass
    
    def calcular(self):
        """Retorna um dicionário com todos os cálculos"""
        return {
            'area_mdf': self.calcular_area_mdf(),
            'metragem_fita': self.calcular_metragem_fita(),
        }