from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.sites import site as admin_site
from .models import Orcamento, Ambiente
import json

@staff_member_required
def orcamento_create(request):
    if request.method == 'GET':
        # Página do formulário
        context = {
            **admin_site.each_context(request),
            'opts': Orcamento._meta,
            'title': 'Adicionar Orçamento',
            'changelist_url': reverse('admin:marcenaria_orcamento_changelist'),
            'status_choices': Orcamento.STATUS_CHOICES,
        }
        return render(request, 'admin/marcenaria/orcamento/new.html', context)
    
    elif request.method == 'POST':
        # Debug dos dados recebidos
        print("POST data:", dict(request.POST))
        
        # Processar dados manualmente
        cliente = request.POST.get('cliente', '').strip()
        status = request.POST.get('status', 'RASCUNHO')
        ambientes_json = request.POST.get('ambientes_json', '[]')
        
        print(f"Cliente: '{cliente}'")
        print(f"Status: '{status}'")
        print(f"Ambientes JSON: '{ambientes_json}'")
        
        # Validações manuais
        errors = {}
        
        if not cliente:
            errors['cliente'] = 'Cliente é obrigatório'
            
        if status not in [choice[0] for choice in Orcamento.STATUS_CHOICES]:
            errors['status'] = 'Status inválido'
            
        # Validar ambientes
        ambientes_nomes = []
        try:
            ambientes_data = json.loads(ambientes_json)
            print(f"Ambientes data parsed: {ambientes_data}")
            
            if not isinstance(ambientes_data, list):
                errors['ambientes'] = 'Formato de ambientes inválido'
            else:
                for item in ambientes_data:
                    print(f"Processando item: {item}")
                    if isinstance(item, dict) and 'nome' in item:
                        nome = str(item['nome']).strip()
                        if nome:
                            ambientes_nomes.append(nome)
                            print(f"Ambiente adicionado: '{nome}'")
                            
        except json.JSONDecodeError as e:
            print(f"Erro JSON: {e}")
            errors['ambientes'] = 'JSON de ambientes inválido'
        
        print(f"Ambientes finais: {ambientes_nomes}")
        print(f"Errors: {errors}")
        
        # Se há erros, renderizar novamente com erros
        if errors:
            context = {
                **admin_site.each_context(request),
                'opts': Orcamento._meta,
                'title': 'Adicionar Orçamento',
                'changelist_url': reverse('admin:marcenaria_orcamento_changelist'),
                'status_choices': Orcamento.STATUS_CHOICES,
                'errors': errors,
                'cliente': cliente,
                'status': status,
                'ambientes_json': ambientes_json,
            }
            return render(request, 'admin/marcenaria/orcamento/new.html', context, status=400)
        
        # Criar orçamento
        orcamento = Orcamento.objects.create(
            cliente=cliente,
            status=status
        )
        print(f"Orçamento criado: {orcamento.numero}")
        
        # Criar ambientes
        ambientes_criados = 0
        for nome in ambientes_nomes:
            ambiente = Ambiente.objects.create(
                orcamento=orcamento,
                nome=nome
            )
            print(f"Ambiente criado: {ambiente.nome}")
            ambientes_criados += 1
        
        messages.success(request, f'Orçamento {orcamento.numero} criado com sucesso com {ambientes_criados} ambiente(s).')
        return redirect(reverse('admin:marcenaria_orcamento_change', args=[orcamento.pk]))
    
    else:
        return redirect('admin:marcenaria_orcamento_changelist')
