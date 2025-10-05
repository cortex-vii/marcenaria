"""
Dados iniciais para tipos de componentes e PEÇAS da marcenaria
"""

# Tipos de COMPONENTES (MDF, FITA, etc.) - Código formato: AC-XXX
TIPOS_COMPONENTES = [
    {
        'codigo': 'AC-001',
        'nome': 'MDF',
        'descricao': 'Medium Density Fiberboard - Placas de fibra de madeira'
    },
    {
        'codigo': 'AC-002',
        'nome': 'FITA',
        'descricao': 'Fitas de borda para acabamento'
    },
    {
        'codigo': 'AC-003',
        'nome': 'COLA',
        'descricao': 'Colas e adesivos para marcenaria'
    },
    {
        'codigo': 'AC-004',
        'nome': 'CORREDIÇAS',
        'descricao': 'Corrediças para gavetas e portas'
    },
    {
        'codigo': 'AC-005',
        'nome': 'DOBRADIÇA',
        'descricao': 'Dobradiças para portas e móveis'
    },
    {
        'codigo': 'AC-006',
        'nome': 'PARAFUSOS',
        'descricao': 'Parafusos diversos para montagem'
    },
]

# Tipos de Peças (Partes dos móveis) - Código formato: PC-XXX
TIPOS_PECAS = [
    {
        'codigo': 'PC-001',
        'nome': 'Base dupla',
        'descricao': 'Base dupla para móveis'
    },
    {
        'codigo': 'PC-002',
        'nome': 'Base simples',
        'descricao': 'Base simples para móveis'
    },
    {
        'codigo': 'PC-003',
        'nome': 'Base engrossada',
        'descricao': 'Base engrossada para móveis'
    },
    {
        'codigo': 'PC-004',
        'nome': 'Fundo simples',
        'descricao': 'Fundo simples para móveis'
    },
    {
        'codigo': 'PC-005',
        'nome': 'Gaveta',
        'descricao': 'Gavetas para móveis'
    },
    {
        'codigo': 'PC-006',
        'nome': 'Lateral dupla',
        'descricao': 'Lateral dupla para móveis'
    },
    {
        'codigo': 'PC-007',
        'nome': 'Lateral engrossada',
        'descricao': 'Lateral engrossada para móveis'
    },
    {
        'codigo': 'PC-008',
        'nome': 'Lateral externa',
        'descricao': 'Lateral externa para móveis'
    },
    {
        'codigo': 'PC-009',
        'nome': 'Lateral simples',
        'descricao': 'Lateral simples para móveis'
    },
    {
        'codigo': 'PC-010',
        'nome': 'Porta de abrir',
        'descricao': 'Portas que abrem com dobradiças'
    },
    {
        'codigo': 'PC-011',
        'nome': 'Porta de correr',
        'descricao': 'Portas de correr com trilhos'
    },
    {
        'codigo': 'PC-012',
        'nome': 'Roda forro',
        'descricao': 'Rodas para forro de móveis'
    },
    {
        'codigo': 'PC-013',
        'nome': 'Roda pé',
        'descricao': 'Rodas para pés de móveis'
    },
]

# Fornecedores - Código formato: FOR-XXX
FORNECEDORES = [
    {
        'codigo': 'FOR-001',
        'nome': 'Madeireira Tocantins Ltda',
        'cnpj': '12.345.678/0001-90',
        'contato': 'João Silva',
        'telefone': '(11) 3456-7890',
        'email': 'joao@madeireito.com.br',
        'endereco': 'Rua das Madeiras, 123 - Tocantins, TO'
    },
    {
        'codigo': 'FOR-002',
        'nome': 'Ferragens Industriais S.A.',
        'cnpj': '98.765.432/0001-10',
        'contato': 'Maria Santos',
        'telefone': '(11) 9876-5432',
        'email': 'maria@ferragens.com.br',
        'endereco': 'Av. Industrial, 456 - São Paulo, SP'
    },
    {
        'codigo': 'FOR-003',
        'nome': 'Distribuidora de Madeiras Norte',
        'cnpj': '11.222.333/0001-44',
        'contato': 'Carlos Oliveira',
        'telefone': '(85) 1234-5678',
        'email': 'carlos@madeiranorte.com.br',
        'endereco': 'Rua da Madeira, 789 - Fortaleza, CE'
    },
]