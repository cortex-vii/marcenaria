from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from money import Money

class TipoComponente(models.Model):
    """Model para tipos de componentes (MDF, FITA, etc.)"""
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Componente")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Tipo de Componente"
        verbose_name_plural = "Tipos de Componentes"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

class TipoPeca(models.Model):
    """Model para tipos de peças"""
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Peça")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Tipo de Peça"
        verbose_name_plural = "Tipos de Peças"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

class Fornecedor(models.Model):
    """Model para fornecedores"""
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    nome = models.CharField(max_length=200, verbose_name="Nome")
    cnpj = models.CharField(max_length=18, blank=True, null=True, verbose_name="CNPJ")
    contato = models.CharField(max_length=100, blank=True, null=True, verbose_name="Pessoa de Contato")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    endereco = models.TextField(blank=True, null=True, verbose_name="Endereço")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

class Orcamento(models.Model):
    """Model para orçamentos"""
    STATUS_CHOICES = [
        ('RASCUNHO', 'Rascunho'),
        ('EM_ANALISE', 'Em Análise'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
        ('CONCLUIDO', 'Concluído'),
    ]
    
    numero = models.CharField(max_length=50, unique=True, blank=True, verbose_name="Número do Orçamento")
    cliente = models.CharField(max_length=200, verbose_name="Cliente")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RASCUNHO', verbose_name="Status")
    data_validade = models.DateField(blank=True, null=True, verbose_name="Data de Validade")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Orçamento"
        verbose_name_plural = "Orçamentos"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """Gera número automaticamente se não fornecido"""
        if not self.numero:
            from datetime import datetime
            timestamp = int(datetime.now().timestamp() * 1000)
            self.numero = f'ORC-{timestamp}'
            
            # Garantir unicidade (caso muito raro de conflito)
            while Orcamento.objects.filter(numero=self.numero).exists():
                import time
                time.sleep(0.001)  # Espera 1ms
                timestamp = int(datetime.now().timestamp() * 1000)
                self.numero = f'ORC-{timestamp}'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero} - {self.cliente}"

class Ambiente(models.Model):
    """Model para ambientes do orçamento"""
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='ambientes', verbose_name="Orçamento")
    nome = models.CharField(max_length=100, verbose_name="Nome do Ambiente")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Ambiente"
        verbose_name_plural = "Ambientes"
        ordering = ['nome']

    def __str__(self):
        return f"{self.orcamento.numero} - {self.nome}"

class Movel(models.Model):
    """Model para móveis do ambiente (ex: Mesa, Armário, etc.)"""
    ambiente = models.ForeignKey(Ambiente, on_delete=models.CASCADE, related_name='moveis', verbose_name="Ambiente")
    nome = models.CharField(max_length=200, verbose_name="Nome do Móvel")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Móvel"
        verbose_name_plural = "Móveis"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Componente(models.Model):
    """Model para os componentes (materiais) como chapas, fitas, etc."""
    UNIDADE_MEDIDA_CHOICES = [
        ('QUADRADO', 'Metro Quadrado (m²)'),
        ('LINEAR', 'Metro Linear (m)'),
        ('LIQUIDO', 'Mililitros (ml)'),
        ('UNIDADE', 'Unidade (un)'),
    ]

    nome = models.CharField(
        max_length=200, 
        verbose_name="Nome do Componente",
        help_text="Nome específico deste componente (ex: 'Chapa MDF 18mm Branca 2,75x1,83m')",

    )
    tipo_componente = models.ForeignKey(TipoComponente, on_delete=models.PROTECT, verbose_name="Tipo de Componente")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Fornecedor")
    
    preco_bruto = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))], 
        verbose_name="Preço Bruto Total",
        help_text="Preço total pago pelo componente",
        default=Decimal('0.01')
    )
    
    # Campo calculado automaticamente
    custo_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=4, 
        verbose_name="Custo por m²/m/ml/unidade",
        help_text="Calculado automaticamente ao salvar",
        default=Decimal('0.0000'),
        editable=False
    )
    
    unidade_medida = models.CharField(
        max_length=10, 
        choices=UNIDADE_MEDIDA_CHOICES, 
        verbose_name="Unidade de Medida",
        default='UNIDADE'
    )

    # --- Campos para Metro Quadrado (m²) ---
    altura = models.DecimalField(
        max_digits=7, decimal_places=3, null=True, blank=True, 
        verbose_name="Altura (m)", 
        help_text="Usar apenas para Metro Quadrado"
    )
    largura = models.DecimalField(
        max_digits=7, decimal_places=3, null=True, blank=True, 
        verbose_name="Largura (m)", 
        help_text="Usar apenas para Metro Quadrado"
    )
    profundidade = models.DecimalField(
        max_digits=7, decimal_places=3, null=True, blank=True, 
        verbose_name="Profundidade (m)", 
        help_text="Usar apenas para Metro Quadrado"
    )

    # --- Campo para Metro Linear (m) ---
    comprimento = models.DecimalField(
        max_digits=7, decimal_places=3, null=True, blank=True, 
        verbose_name="Comprimento (m)", 
        help_text="Usar apenas para Metro Linear"
    )

    # --- Campo para Líquidos (ml) ---
    volume_ml = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True, 
        verbose_name="Volume (ml)", 
        help_text="Usar apenas para Líquidos"
    )

    # --- Campo para Unidades ---
    quantidade = models.PositiveIntegerField(
        null=True, 
        blank=True,
        verbose_name="Quantidade", 
        help_text="Usar apenas para Unidades"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Componente (Material)"
        verbose_name_plural = "Componentes (Materiais)"
        ordering = ['tipo_componente__nome']

    def __str__(self):
        return self.nome

    @property
    def preco_bruto_money(self):
        """Retorna o preço bruto como objeto Money"""
        return Money(self.preco_bruto, 'BRL')

    @property
    def custo_unitario_money(self):
        """Retorna o custo unitário como objeto Money"""
        return Money(self.custo_unitario, 'BRL')

    def calcular_custo_unitario(self):
        """Calcula o custo unitário baseado no preço bruto e dimensões"""
        if self.preco_bruto <= 0:
            return Decimal('0.0000')
            
        if self.unidade_medida == 'QUADRADO' and self.altura and self.largura:
            # Para m²: custo por metro quadrado (SEM multiplicar pela profundidade)
            area_total = self.altura * self.largura
            # Profundidade é apenas informativa (espessura), não afeta o cálculo de área
            if area_total > 0:
                return self.preco_bruto / area_total
            
        elif self.unidade_medida == 'LINEAR' and self.comprimento:
            # Para m: custo por metro linear
            if self.comprimento > 0:
                return self.preco_bruto / self.comprimento
            
        elif self.unidade_medida == 'LIQUIDO' and self.volume_ml:
            # Para ml: custo por mililitro
            if self.volume_ml > 0:
                return self.preco_bruto / self.volume_ml
            
        elif self.unidade_medida == 'UNIDADE' and self.quantidade:
            # Para unidades: custo por unidade
            if self.quantidade > 0:
                return self.preco_bruto / Decimal(str(self.quantidade))
            
        return Decimal('0.0000')

    def save(self, *args, **kwargs):
        """Override do save para calcular o custo unitário automaticamente"""
        self.custo_unitario = self.calcular_custo_unitario()
        super().save(*args, **kwargs)

    def clean(self):
        """Validação customizada para garantir que apenas os campos corretos sejam preenchidos"""
        from django.core.exceptions import ValidationError
        
        errors = {}
        
        if self.unidade_medida == 'QUADRADO':
            if not self.altura or not self.largura:
                errors['__all__'] = 'Para Metro Quadrado, altura e largura são obrigatórios.'
            if self.comprimento or self.volume_ml:
                errors['__all__'] = 'Para Metro Quadrado, preencha apenas altura, largura e profundidade.'
                
        elif self.unidade_medida == 'LINEAR':
            if not self.comprimento:
                errors['comprimento'] = 'Para Metro Linear, o comprimento é obrigatório.'
            if self.altura or self.largura or self.volume_ml:
                errors['__all__'] = 'Para Metro Linear, preencha apenas o comprimento.'
                
        elif self.unidade_medida == 'LIQUIDO':
            if not self.volume_ml:
                errors['volume_ml'] = 'Para Líquidos, o volume em ml é obrigatório.'
            if self.altura or self.largura or self.comprimento:
                errors['__all__'] = 'Para Líquidos, preencha apenas o volume em ml.'
                
        elif self.unidade_medida == 'UNIDADE':
            if not self.quantidade or self.quantidade < 1:
                errors['quantidade'] = 'Para Unidades, a quantidade deve ser maior que zero.'
            if self.altura or self.largura or self.comprimento or self.volume_ml:
                errors['__all__'] = 'Para Unidades, preencha apenas a quantidade.'
        
        if errors:
            raise ValidationError(errors)



