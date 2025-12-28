from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.sites import site as admin_site
from django.http import JsonResponse
from django.utils import timezone
from decimal import Decimal
from .models import Orcamento, Ambiente, TipoPeca, Componente, Movel, TipoComponente
from .utils.rule_manager import RuleManager
from .models import Componente
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST



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
            
        # Validar e processar ambientes
        ambientes_data = []
        valor_total = Decimal('0.00')
        
        try:
            ambientes_parsed = json.loads(ambientes_json)
            print(f"Ambientes data parsed: {ambientes_parsed}")
            
            if not isinstance(ambientes_parsed, list):
                errors['ambientes'] = 'Formato de ambientes inválido'
            else:
                for ambiente_item in ambientes_parsed:
                    print(f"Processando ambiente: {ambiente_item}")
                    
                    if isinstance(ambiente_item, dict) and 'nome' in ambiente_item:
                        nome_ambiente = str(ambiente_item['nome']).strip()
                        if nome_ambiente:
                            moveis_processados = []
                            
                            # Processar móveis do ambiente
                            for movel_item in ambiente_item.get('moveis', []):
                                print(f"Processando móvel: {movel_item}")
                                
                                if isinstance(movel_item, dict) and 'nome' in movel_item:
                                    nome_movel = str(movel_item['nome']).strip()
                                    if nome_movel:
                                        pecas_processadas = []
                                        
                                        # Processar peças do móvel
                                        for peca_item in movel_item.get('pecas', []):
                                            print(f"Processando peça: {peca_item}")
                                            
                                            if isinstance(peca_item, dict):
                                                # Obter o componente do banco
                                                componente_id = peca_item.get('componente_id')
                                                if componente_id:
                                                    try:
                                                        componente = Componente.objects.get(id=componente_id)
                                                        
                                                        # Executar cálculo usando RuleManager
                                                        tipo_peca_codigo = peca_item.get('tipo_codigo')
                                                        dados_calculo = peca_item.get('dados_calculo', {})
                                                        
                                                        resultado_calculo = RuleManager.calcular(
                                                            tipo_peca_codigo, 
                                                            dados_calculo, 
                                                            componente
                                                        )
                                                        
                                                        # Calcular custo total
                                                        custo_total = Decimal('0.00')
                                                        if resultado_calculo.get('sucesso'):
                                                            quantidade_utilizada = resultado_calculo.get('quantidade_utilizada', 0)
                                                            custo_unitario = componente.custo_unitario
                                                            custo_total = Decimal(str(quantidade_utilizada)) * custo_unitario
                                                            resultado_calculo['custo_total'] = float(custo_total)
                                                            valor_total += custo_total
                                                        
                                                        # Estrutura final da peça
                                                        peca_processada = {
                                                            'tipo_codigo': tipo_peca_codigo,
                                                            'tipo_nome': peca_item.get('tipo_nome'),
                                                            'componente_id': componente_id,
                                                            'componente_nome': peca_item.get('componente_nome'),
                                                            'componente_preco_unitario': float(componente.custo_unitario),
                                                            'dados_calculo': dados_calculo,
                                                            'resultado_calculo': resultado_calculo,
                                                            'resumo': peca_item.get('resumo')
                                                        }
                                                        
                                                        pecas_processadas.append(peca_processada)
                                                        print(f"Peça processada com custo: R$ {custo_total}")
                                                        
                                                    except Componente.DoesNotExist:
                                                        print(f"Componente {componente_id} não encontrado")
                                                        continue
                                        
                                        # Estrutura final do móvel
                                        movel_processado = {
                                            'nome': nome_movel,
                                            'pecas': pecas_processadas
                                        }
                                        moveis_processados.append(movel_processado)
                            
                            # Estrutura final do ambiente
                            ambiente_processado = {
                                'nome': nome_ambiente,
                                'moveis': moveis_processados
                            }
                            ambientes_data.append(ambiente_processado)
                            print(f"Ambiente processado: '{nome_ambiente}' com {len(moveis_processados)} móveis")
                            
        except json.JSONDecodeError as e:
            print(f"Erro JSON: {e}")
            errors['ambientes'] = 'JSON de ambientes inválido'
        except Exception as e:
            print(f"Erro no processamento: {e}")
            errors['ambientes'] = f'Erro no processamento dos dados: {str(e)}'
        
        print(f"Ambientes finais: {len(ambientes_data)} ambientes")
        print(f"Valor total calculado: R$ {valor_total}")
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
        
        # Estrutura final dos dados do orçamento
        dados_orcamento_final = {
            'ambientes': ambientes_data,
            'valor_total': float(valor_total),
            'versao': '1.0',
            'data_calculo': timezone.now().isoformat()
        }
        
        # Criar orçamento com dados JSON
        orcamento = Orcamento.objects.create(
            cliente=cliente,
            status=status,
            dados_orcamento=dados_orcamento_final,
            valor_total=valor_total
        )
        print(f"Orçamento criado: {orcamento.numero} - Valor: R$ {orcamento.valor_total}")
        
        # Criar ambientes básicos (para compatibilidade)
        ambientes_criados = 0
        for ambiente_data in ambientes_data:
            ambiente = Ambiente.objects.create(
                orcamento=orcamento,
                nome=ambiente_data['nome']
            )
            print(f"Ambiente criado: {ambiente.nome}")
            ambientes_criados += 1
            
            # Criar móveis básicos (para compatibilidade)
            for movel_data in ambiente_data.get('moveis', []):
                movel = Movel.objects.create(
                    ambiente=ambiente,
                    nome=movel_data['nome']
                )
                print(f"Móvel criado: {movel.nome}")
        
        messages.success(request, f'Orçamento {orcamento.numero} criado com sucesso! Valor total: R$ {orcamento.valor_total:.2f}')
        return redirect(reverse('admin:marcenaria_orcamento_change', args=[orcamento.pk]))
    
    else:
        return redirect('admin:marcenaria_orcamento_changelist')


@staff_member_required
def get_componentes_por_tipo_peca(request, tipo_peca_codigo):
    """
    API que retorna os componentes disponíveis e adicionais para um tipo de peça,
    sendo os adicionais separados por código.
    """
    try:
        # Componentes principais
        componentes_codigos = RuleManager.get_componentes_disponiveis(tipo_peca_codigo)
        componentes = Componente.objects.filter(
            tipo_componente__codigo__in=componentes_codigos,
            tipo_componente__ativo=True
        ).select_related('tipo_componente', 'fornecedor')

        componentes_data = []
        for comp in componentes:
            componentes_data.append({
                'id': comp.id,
                'nome': comp.nome,
                'tipo_codigo': comp.tipo_componente.codigo,
                'tipo_nome': comp.tipo_componente.nome,
                'fornecedor_nome': comp.fornecedor.nome if comp.fornecedor else 'Sem fornecedor',
                'preco_bruto': float(comp.preco_bruto),
                'custo_unitario': float(comp.custo_unitario),
                'unidade_medida': comp.get_unidade_medida_display(),
            })

        # Componentes adicionais separados por código
        adicionais_codigos = []
        rule_class = RuleManager.get_rule_class(tipo_peca_codigo)
        if rule_class and hasattr(rule_class, 'COMPONENTES_ADICIONAIS'):
            adicionais_codigos = rule_class.COMPONENTES_ADICIONAIS

        adicionais_dict = {}
        for codigo in adicionais_codigos:
            tipo = TipoComponente.objects.filter(codigo=codigo).first()
            nome = tipo.nome if tipo else ""
            componentes = Componente.objects.filter(tipo_componente__codigo=codigo, tipo_componente__ativo=True).select_related('tipo_componente', 'fornecedor')
            adicionais_dict[codigo] = {
                "codigo": codigo,
                "nome": nome,
                "componentes": [
                    {
                        "id": c.id,
                        "nome": c.nome,
                        "tipo_codigo": c.tipo_componente.codigo,
                        "tipo_nome": c.tipo_componente.nome,
                        "fornecedor_nome": c.fornecedor.nome if c.fornecedor else 'Sem fornecedor',
                        "preco_bruto": float(c.preco_bruto),
                        "custo_unitario": float(c.custo_unitario),
                        "unidade_medida": c.get_unidade_medida_display(),
                    }
                    for c in componentes
                ]
            }

        return JsonResponse({
            'sucesso': True,
            'componentes': componentes_data,
            'componentes_adicionais': adicionais_dict
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

@staff_member_required
@require_POST
def calcular_peca_api(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        tipo_peca_codigo = data.get('tipo_peca_codigo')
        dados_calculo = data.get('dados_calculo', {})
        componente_id = data.get('componente_id')
        componentes_adicionais = data.get('componentes_adicionais', None)

        print("Dados recebidos para cálculo da peça--------------:")
        print(f"Tipo da peça base simples/base dupla/fundo etc: {tipo_peca_codigo}")
        print(f"Componente principal: {componente_id}")
        print(f"Dados para os cálculos das peças: {dados_calculo}")
        print(f"Componentes Adicionais das peças: {componentes_adicionais}")
        print("Dados recebidos para cálculo da peça--------------:")
        
        
        if not tipo_peca_codigo or not componente_id:
            return JsonResponse({'sucesso': False, 'erro': 'tipo_peca_codigo e componente_id são obrigatórios'}, status=400)

        # Buscar o componente principal pelo id
        componente = Componente.objects.get(id=componente_id)

        # Buscar os componentes adicionais pelo id, se houver
        adicionais_objs = None
        if componentes_adicionais and isinstance(componentes_adicionais, list) and len(componentes_adicionais) > 0:
            adicionais_objs = []
            for adicional_id in componentes_adicionais:
                try:
                    adicional_obj = Componente.objects.get(id=adicional_id)
                    adicionais_objs.append(adicional_obj)
                except Componente.DoesNotExist:
                    continue

        # Chama a regra de cálculo passando o objeto do adicional (ou lista de objetos)
        rule_class = RuleManager.get_rule_class(tipo_peca_codigo)
        if rule_class and hasattr(rule_class, 'calcular'):
            # Se houver adicionais, passar a lista, senão None
            resultado = rule_class.calcular(dados_calculo, componente, adicionais_objs)
            resultado['sucesso'] = True if not resultado.get('erro') else False
            return JsonResponse(resultado)
        else:
            return JsonResponse({'sucesso': False, 'erro': 'Regra de cálculo não encontrada'}, status=400)
    except Componente.DoesNotExist:
        return JsonResponse({'sucesso': False, 'erro': 'Componente não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)
