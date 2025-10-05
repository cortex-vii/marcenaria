from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.sites import site as admin_site
from django.http import JsonResponse
from .models import Orcamento, Ambiente, TipoPeca, Componente
from .utils.rule_manager import RuleManager
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
            'tipos_pecas': TipoPeca.objects.filter(ativo=True).order_by('codigo'),
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
        ambientes_data = []
        try:
            ambientes_parsed = json.loads(ambientes_json)
            print(f"Ambientes data parsed: {ambientes_parsed}")
            
            if not isinstance(ambientes_parsed, list):
                errors['ambientes'] = 'Formato de ambientes inválido'
            else:
                for item in ambientes_parsed:
                    print(f"Processando item: {item}")
                    if isinstance(item, dict) and 'nome' in item:
                        nome = str(item['nome']).strip()
                        if nome:
                            # Incluir também os móveis e peças na validação
                            ambiente_data = {
                                'nome': nome,
                                'moveis': item.get('moveis', [])
                            }
                            ambientes_data.append(ambiente_data)
                            print(f"Ambiente adicionado: '{nome}' com {len(ambiente_data['moveis'])} móveis")
                            
        except json.JSONDecodeError as e:
            print(f"Erro JSON: {e}")
            errors['ambientes'] = 'JSON de ambientes inválido'
        
        print(f"Ambientes finais: {len(ambientes_data)} ambientes")
        print(f"Errors: {errors}")
        
        # Se há erros, renderizar novamente com erros
        if errors:
            context = {
                **admin_site.each_context(request),
                'opts': Orcamento._meta,
                'title': 'Adicionar Orçamento',
                'changelist_url': reverse('admin:marcenaria_orcamento_changelist'),
                'status_choices': Orcamento.STATUS_CHOICES,
                'tipos_pecas': TipoPeca.objects.filter(ativo=True).order_by('codigo'),
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
        for ambiente_data in ambientes_data:
            ambiente = Ambiente.objects.create(
                orcamento=orcamento,
                nome=ambiente_data['nome']
            )
            print(f"Ambiente criado: {ambiente.nome}")
            ambientes_criados += 1
            
            # Aqui você pode adicionar lógica para processar móveis e peças
            # Por enquanto vamos só criar os ambientes
            # TODO: Implementar criação de móveis e peças
        
        messages.success(request, f'Orçamento {orcamento.numero} criado com sucesso com {ambientes_criados} ambiente(s).')
        return redirect(reverse('admin:marcenaria_orcamento_change', args=[orcamento.pk]))
    
    else:
        return redirect('admin:marcenaria_orcamento_changelist')


@staff_member_required
def get_componentes_por_tipo_peca(request, tipo_peca_codigo):
    """
    API que retorna os componentes disponíveis para um tipo de peça
    """
    try:
        # Obter componentes disponíveis através do RuleManager
        componentes_codigos = RuleManager.get_componentes_disponiveis(tipo_peca_codigo)
        
        # Buscar os componentes no banco
        componentes = Componente.objects.filter(
            tipo_componente__codigo__in=componentes_codigos,
            tipo_componente__ativo=True
        ).select_related('tipo_componente', 'fornecedor')
        
        # Serializar os dados
        componentes_data = []
        for comp in componentes:
            componentes_data.append({
                'id': comp.id,
                'nome': comp.nome,
                'tipo_nome': comp.tipo_componente.nome,
                'fornecedor_nome': comp.fornecedor.nome if comp.fornecedor else 'Sem fornecedor',
                'preco_bruto': float(comp.preco_bruto),
                'custo_unitario': float(comp.custo_unitario),
                'unidade_medida': comp.get_unidade_medida_display(),
            })
        
        return JsonResponse({
            'sucesso': True,
            'componentes': componentes_data
        })
        
    except Exception as e:
        return JsonResponse({
            'sucesso': False,
            'erro': str(e)
        }, status=400)


@staff_member_required
def get_campos_calculo_peca(request, tipo_peca_codigo):
    """
    API que retorna os campos necessários para cálculo de um tipo de peça
    """
    try:
        # Obter campos através do RuleManager
        campos = RuleManager.get_campos_necessarios(tipo_peca_codigo)
        
        return JsonResponse({
            'sucesso': True,
            'campos': campos
        })
        
    except Exception as e:
        return JsonResponse({
            'sucesso': False,
            'erro': str(e)
        }, status=400)
