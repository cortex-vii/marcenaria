from django.core.management.base import BaseCommand
from marcenaria.models import TipoPeca, TipoComponente, Fornecedor
from marcenaria.data.initial_data import TIPOS_PECAS, TIPOS_COMPONENTES, FORNECEDORES

class Command(BaseCommand):
    help = 'Popula os tipos de peças, componentes e fornecedores iniciais'

    def handle(self, *args, **options):
        
        self.stdout.write('Criando tipos de peças...')
        for item in TIPOS_PECAS:
            tipo, created = TipoPeca.objects.get_or_create(
                codigo=item['codigo'],
                defaults={
                    'nome': item['nome'],
                    'descricao': item['descricao']
                }
            )
            if created:
                self.stdout.write(f'✓ Criado: {item["codigo"]} - {item["nome"]}')
            else:
                self.stdout.write(f'- Já existe: {item["codigo"]} - {item["nome"]}')

        self.stdout.write('\nCriando tipos de componentes...')
        for item in TIPOS_COMPONENTES:
            tipo, created = TipoComponente.objects.get_or_create(
                codigo=item['codigo'],
                defaults={
                    'nome': item['nome'],
                    'descricao': item['descricao']
                }
            )
            if created:
                self.stdout.write(f'✓ Criado: {item["codigo"]} - {item["nome"]}')
            else:
                self.stdout.write(f'- Já existe: {item["codigo"]} - {item["nome"]}')

        self.stdout.write('\nCriando fornecedores...')
        for item in FORNECEDORES:
            fornecedor, created = Fornecedor.objects.get_or_create(
                codigo=item['codigo'],
                defaults={
                    'nome': item['nome'],
                    'cnpj': item['cnpj'],
                    'contato': item['contato'],
                    'telefone': item['telefone'],
                    'email': item['email'],
                    'endereco': item['endereco']
                }
            )
            if created:
                self.stdout.write(f'✓ Criado: {item["codigo"]} - {item["nome"]}')
            else:
                self.stdout.write(f'- Já existe: {item["codigo"]} - {item["nome"]}')

        self.stdout.write(
            self.style.SUCCESS('\n✅ Dados iniciais criados com sucesso!')
        )