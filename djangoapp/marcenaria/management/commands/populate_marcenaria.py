from django.core.management.base import BaseCommand
from marcenaria.models import TipoPeca, TipoComponente, Fornecedor
from marcenaria.data.initial_data import TIPOS_COMPONENTES, TIPOS_ACESSORIOS, FORNECEDORES

# docker exec -it marcenaria_cortex_djangoservice sh
# python manage.py populate_marcenaria - para executar
class Command(BaseCommand):
    help = 'Popula os tipos de peças, componentes e fornecedores iniciais'

    def handle(self, *args, **options):
        
        self.stdout.write('Criando tipos de peças...')
        for nome, descricao in TIPOS_COMPONENTES:
            tipo, created = TipoPeca.objects.get_or_create(
                nome=nome,
                defaults={'descricao': descricao}
            )
            if created:
                self.stdout.write(f'✓ Criado: {nome}')
            else:
                self.stdout.write(f'- Já existe: {nome}')

        self.stdout.write('\nCriando tipos de componentes...')
        for nome, descricao in TIPOS_ACESSORIOS:
            tipo, created = TipoComponente.objects.get_or_create(
                nome=nome,
                defaults={'descricao': descricao}
            )
            if created:
                self.stdout.write(f'✓ Criado: {nome}')
            else:
                self.stdout.write(f'- Já existe: {nome}')

        self.stdout.write('\nCriando fornecedores...')
        for fornecedor_data in FORNECEDORES:
            fornecedor, created = Fornecedor.objects.get_or_create(
                cnpj=fornecedor_data['cnpj'],
                defaults=fornecedor_data
            )
            if created:
                self.stdout.write(f'✓ Criado: {fornecedor_data["nome"]}')
            else:
                self.stdout.write(f'- Já existe: {fornecedor_data["nome"]}')

        self.stdout.write(
            self.style.SUCCESS('\n✅ Dados iniciais criados com sucesso!')
        )