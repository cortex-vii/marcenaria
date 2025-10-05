from .base_dupla import BaseDuplaRule
from .base_engrossada import BaseEngrossadaRule
from .base_simples import BaseSimplesRule
from .lateral_dupla import LateralDuplaRule
from .lateral_engrossada import LateralEngrossadaRule
from .lateral_simples import LateralSimplesRule
from .fundo_simples import FundoSimplesRule
from .gaveta import GavetaRule
from .porta_abrir import PortaAbrirRule
from .porta_correr import PortaCorrerRule

# Mapeamento de tipos de componentes para suas regras
REGRAS_COMPONENTES = {
    'Base dupla': BaseDuplaRule,
    'Base engrossada': BaseEngrossadaRule,
    'Base simples': BaseSimplesRule,
    'Lateral dupla': LateralDuplaRule,
    'Lateral engrossada': LateralEngrossadaRule,
    'Lateral simples': LateralSimplesRule,
    'Fundo simples': FundoSimplesRule,
    'Gaveta': GavetaRule,
    'Porta de abrir': PortaAbrirRule,
    'Porta de correr': PortaCorrerRule,
}

def obter_regra(tipo_componente_nome):
    """Retorna a classe de regra apropriada para o tipo de componente"""
    return REGRAS_COMPONENTES.get(tipo_componente_nome)