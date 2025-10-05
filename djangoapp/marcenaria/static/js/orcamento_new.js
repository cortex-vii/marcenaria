document.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('ambienteNome');
  const btn = document.getElementById('btnAddAmbiente');
  const container = document.getElementById('ambientesContainer');
  const hidden = document.getElementById('ambientesJson');

  if (!input || !btn || !container || !hidden) {
    console.error('Um ou mais elementos do formulário de ambientes não foram encontrados.');
    return;
  }

  let ambientes = [];
  let currentAmbienteIndex = null;
  let currentMovelIndex = null;
  let currentCalculoTimeout = null;

  try {
    ambientes = JSON.parse(hidden.value || '[]');
  } catch (e) {
    console.error('Erro ao carregar ambientes do campo hidden:', e);
    ambientes = [];
  }

  // ========== FUNÇÕES DE RENDERIZAÇÃO ==========
  
  function render() {
    container.innerHTML = '';
    
    if (ambientes.length === 0) {
      container.innerHTML = '<div class="empty-state">Nenhum ambiente adicionado</div>';
    } else {
      ambientes.forEach((ambiente, ambIdx) => {
        const ambienteDiv = document.createElement('div');
        ambienteDiv.className = 'ambiente-item';
        ambienteDiv.innerHTML = `
          <div class="ambiente-header">
            <h3>${ambiente.nome}</h3>
            <div class="ambiente-actions">
              <button type="button" class="btn btn-primary btn-sm" data-ambiente="${ambIdx}" data-action="add-movel">
                Adicionar Móvel
              </button>
              <button type="button" class="btn btn-danger btn-sm" data-ambiente="${ambIdx}" data-action="remove">
                Remover Ambiente
              </button>
            </div>
          </div>
          <div class="moveis-container" id="moveis-${ambIdx}">
            ${renderMoveis(ambiente.moveis || [], ambIdx)}
          </div>
        `;
        container.appendChild(ambienteDiv);
      });
    }
    
    hidden.value = JSON.stringify(ambientes);
    atualizarResumo();
  }

  function renderMoveis(moveis, ambienteIdx) {
    if (!moveis || moveis.length === 0) {
      return '<div class="empty-moveis">Nenhum móvel adicionado</div>';
    }

    return moveis.map((movel, movelIdx) => `
      <div class="movel-item">
        <div class="movel-header">
          <h4>${movel.nome}</h4>
          <div class="movel-actions">
            <button type="button" class="btn btn-primary btn-sm" 
                    data-ambiente="${ambienteIdx}" 
                    data-movel="${movelIdx}" 
                    data-action="add-peca">
              Adicionar Peça
            </button>
            <button type="button" class="btn btn-danger btn-sm" 
                    data-ambiente="${ambienteIdx}" 
                    data-movel="${movelIdx}" 
                    data-action="remove-movel">
              Remover
            </button>
          </div>
        </div>
        <div class="pecas-container">
          ${renderPecas(movel.pecas || [], ambienteIdx, movelIdx)}
        </div>
      </div>
    `).join('');
  }

  function renderPecas(pecas, ambienteIdx, movelIdx) {
    if (!pecas || pecas.length === 0) {
      return '<div class="empty-pecas">Nenhuma peça adicionada</div>';
    }

    return pecas.map((peca, pecaIdx) => {
      let calculoInfo = '';
      
      if (peca.resultado_calculo && peca.resultado_calculo.sucesso) {
        const resultado = peca.resultado_calculo;
        const custo = resultado.custo_total || 0;
        
        calculoInfo = `
          <div class="peca-calculo">
            <div class="peca-quantidade">${resultado.resumo || ''}</div>
            <div class="peca-custo">Custo: R$ ${custo.toFixed(2)}</div>
          </div>
        `;
      }

      return `
        <div class="peca-item">
          <div class="peca-info">
            <div class="peca-nome">${peca.tipo_nome} - ${peca.componente_nome}</div>
            <div class="peca-detalhes">${peca.resumo || 'Calculando...'}</div>
            ${calculoInfo}
          </div>
          <div class="peca-actions">
            <button type="button" class="btn btn-danger btn-xs" 
                    data-ambiente="${ambienteIdx}"
                    data-movel="${movelIdx}"
                    data-peca="${pecaIdx}" 
                    data-action="remove-peca">
              Remover
            </button>
          </div>
        </div>
      `;
    }).join('');
  }

  // ========== FUNÇÕES DE RESUMO ==========

  function atualizarResumo() {
    let totalAmbientes = ambientes.length;
    let totalMoveis = 0;
    let totalPecasFisicas = 0; // Mudança: contar peças físicas, não registros
    let valorTotal = 0;

    // Debug para verificar a estrutura
    console.log('Calculando resumo:', ambientes);

    ambientes.forEach((ambiente, ambIdx) => {
      const moveis = ambiente.moveis || [];
      totalMoveis += moveis.length;
      
      moveis.forEach((movel, movelIdx) => {
        const pecas = movel.pecas || [];
        
        pecas.forEach((peca, pecaIdx) => {
          // Contar quantidade física de peças, não registros
          const quantidadeFisica = parseInt(peca.dados_calculo?.quantidade || 1);
          totalPecasFisicas += quantidadeFisica;
          
          console.log(`Ambiente ${ambIdx}, Móvel ${movelIdx}, Peça ${pecaIdx}: ${quantidadeFisica} peças físicas`);
          
          if (peca.resultado_calculo && peca.resultado_calculo.custo_total) {
            const custo = parseFloat(peca.resultado_calculo.custo_total);
            valorTotal += custo;
            console.log(`Peça ${pecaIdx}: R$ ${custo}`);
          }
        });
      });
    });

    console.log(`Total: ${totalAmbientes} ambientes, ${totalMoveis} móveis, ${totalPecasFisicas} peças físicas, R$ ${valorTotal}`);

    // Atualizar estatísticas
    document.getElementById('totalAmbientes').textContent = totalAmbientes;
    document.getElementById('totalMoveis').textContent = totalMoveis;
    document.getElementById('totalPecas').textContent = totalPecasFisicas; // Usar peças físicas
    document.getElementById('valorTotal').textContent = `R$ ${valorTotal.toFixed(2).replace('.', ',')}`;

    // Atualizar detalhes
    atualizarResumoDetalhes();
  }

  function atualizarResumoDetalhes() {
    const container = document.getElementById('resumoDetalhes');
    
    if (ambientes.length === 0) {
      container.innerHTML = '<div class="empty-state" style="margin: 0; padding: 20px 0; border: none;">Nenhum item adicionado</div>';
      return;
    }

    let html = '';
    
    ambientes.forEach(ambiente => {
      const moveis = ambiente.moveis || [];
      let custoAmbiente = 0;
      
      moveis.forEach(movel => {
        const pecas = movel.pecas || [];
        
        pecas.forEach(peca => {
          if (peca.resultado_calculo && peca.resultado_calculo.custo_total) {
            custoAmbiente += parseFloat(peca.resultado_calculo.custo_total);
          }
        });
      });

      html += `
        <div class="ambiente-resumo">
          <div class="ambiente-resumo-nome">
            ${ambiente.nome} - R$ ${custoAmbiente.toFixed(2)}
          </div>
          ${moveis.map(movel => {
            // Calcular total de peças físicas do móvel
            const totalPecasFisicasMovel = (movel.pecas || []).reduce((acc, peca) => {
              const quantidade = parseInt(peca.dados_calculo?.quantidade || 1);
              return acc + quantidade;
            }, 0);
            
            return `
              <div class="movel-resumo">
                📦 ${movel.nome} (${totalPecasFisicasMovel} peças)
              </div>
            `;
          }).join('')}
        </div>
      `;
    });
    
    container.innerHTML = html;
  }

  // ========== FUNÇÕES DE CÁLCULO ==========

  async function calcularPeca(tipoPecaCodigo, dadosCalculo, componenteData) {
    try {
      // Simular chamada de API para cálculo
      // Em produção, você faria uma chamada real para o backend
      
      const response = await fetch('/marcenaria/api/calcular-peca/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({
          tipo_peca_codigo: tipoPecaCodigo,
          dados_calculo: dadosCalculo,
          componente_id: componenteData.id
        })
      });

      if (response.ok) {
        return await response.json();
      } else {
        // Fallback: cálculo simples no frontend
        return calcularPecaLocal(tipoPecaCodigo, dadosCalculo, componenteData);
      }
    } catch (error) {
      console.log('Usando cálculo local devido a erro:', error);
      return calcularPecaLocal(tipoPecaCodigo, dadosCalculo, componenteData);
    }
  }

  function calcularPecaLocal(tipoPecaCodigo, dadosCalculo, componenteData) {
    // Cálculo simples baseado no tipo de peça
    const quantidade = parseFloat(dadosCalculo.quantidade || 0);
    const altura = parseFloat(dadosCalculo.altura || 0) / 100; // cm para m
    const largura = parseFloat(dadosCalculo.largura || 0) / 100; // cm para m
    
    if (quantidade <= 0 || altura <= 0 || largura <= 0) {
      return {
        sucesso: false,
        erro: 'Dados inválidos para cálculo'
      };
    }

    const areaUnitaria = altura * largura;
    const areaTotal = areaUnitaria * quantidade;
    const custoUnitario = parseFloat(componenteData.custo_unitario || 0);
    const custoTotal = areaTotal * custoUnitario;

    return {
      sucesso: true,
      area_por_peca: areaUnitaria,
      area_total: areaTotal,
      quantidade_utilizada: areaTotal,
      custo_total: custoTotal,
      unidade: 'm²',
      resumo: `${quantidade}x peças de ${(altura*100).toFixed(1)}cm x ${(largura*100).toFixed(1)}cm = ${areaTotal.toFixed(4)} m²`
    };
  }

  function mostrarResultadoCalculo(resultado) {
    const container = document.getElementById('calculoResultado');
    const detalhes = document.getElementById('calculoDetalhes');
    const custo = document.getElementById('calculoCusto');

    if (resultado.sucesso) {
      container.className = 'calculo-resultado calculo-sucesso';
      detalhes.innerHTML = `
        <div>Área por peça: ${resultado.area_por_peca?.toFixed(4) || 0} m²</div>
        <div>Área total: ${resultado.area_total?.toFixed(4) || 0} m²</div>
        <div>${resultado.resumo || ''}</div>
      `;
      custo.textContent = `Custo Total: R$ ${(resultado.custo_total || 0).toFixed(2)}`;
    } else {
      container.className = 'calculo-resultado calculo-erro';
      detalhes.textContent = resultado.erro || 'Erro no cálculo';
      custo.textContent = '';
    }

    container.style.display = 'block';
  }

  async function calcularEmTempoReal() {
    const tipoPeca = document.getElementById('tipoPeca').value;
    const componentePeca = document.getElementById('componentePeca').value;
    
    if (!tipoPeca || !componentePeca) {
      document.getElementById('calculoResultado').style.display = 'none';
      return;
    }

    // Coletar dados dos campos
    const dadosCalculo = {};
    const campos = document.querySelectorAll('#camposCalculoContainer input');
    let camposValidos = true;
    
    for (let campo of campos) {
      const valor = campo.value.trim();
      if (campo.required && !valor) {
        camposValidos = false;
        break;
      }
      dadosCalculo[campo.name] = valor;
    }

    if (!camposValidos) {
      document.getElementById('calculoResultado').style.display = 'none';
      return;
    }

    // Obter dados do componente
    const compOption = document.getElementById('componentePeca').options[document.getElementById('componentePeca').selectedIndex];
    const componenteData = JSON.parse(compOption.dataset.componente);

    // Fazer cálculo
    const resultado = await calcularPeca(tipoPeca, dadosCalculo, componenteData);
    mostrarResultadoCalculo(resultado);
  }

  // ========== FUNÇÕES DE MANIPULAÇÃO DE DADOS ==========

  function addAmbiente() {
    const nome = input.value.trim();
    if (!nome) {
      alert('Digite o nome do ambiente');
      input.focus();
      return;
    }
    
    const existe = ambientes.some(a => a.nome.toLowerCase() === nome.toLowerCase());
    if (existe) {
      alert('Este ambiente já foi adicionado!');
      input.focus();
      return;
    }
    
    ambientes.push({ 
      nome: nome,
      moveis: []
    });
    input.value = '';
    input.focus();
    render();
  }

  function removeAmbiente(idx) {
    if (confirm(`Remover o ambiente "${ambientes[idx].nome}" e todos os seus móveis?`)) {
      ambientes.splice(idx, 1);
      render();
    }
  }

  function addMovel(ambienteIdx, nomeMovel) {
    if (!ambientes[ambienteIdx].moveis) {
      ambientes[ambienteIdx].moveis = [];
    }
    
    ambientes[ambienteIdx].moveis.push({
      nome: nomeMovel,
      pecas: []
    });
    
    render();
  }

  function removeMovel(ambienteIdx, movelIdx) {
    const movel = ambientes[ambienteIdx].moveis[movelIdx];
    if (confirm(`Remover o móvel "${movel.nome}" e todas as suas peças?`)) {
      ambientes[ambienteIdx].moveis.splice(movelIdx, 1);
      render();
    }
  }

  async function addPeca(ambienteIdx, movelIdx, dadosPeca) {
    if (!ambientes[ambienteIdx].moveis[movelIdx].pecas) {
      ambientes[ambienteIdx].moveis[movelIdx].pecas = [];
    }
    
    // Fazer cálculo antes de adicionar
    const componenteData = {
      id: dadosPeca.componente_id,
      nome: dadosPeca.componente_nome,
      custo_unitario: dadosPeca.componente_preco_unitario
    };

    const resultado = await calcularPeca(dadosPeca.tipo_codigo, dadosPeca.dados_calculo, componenteData);
    dadosPeca.resultado_calculo = resultado;
    
    ambientes[ambienteIdx].moveis[movelIdx].pecas.push(dadosPeca);
    render();
  }

  function removePeca(ambienteIdx, movelIdx, pecaIdx) {
    const peca = ambientes[ambienteIdx].moveis[movelIdx].pecas[pecaIdx];
    if (confirm(`Remover a peça "${peca.tipo_nome}"?`)) {
      ambientes[ambienteIdx].moveis[movelIdx].pecas.splice(pecaIdx, 1);
      render();
    }
  }

  // ========== FUNÇÕES DOS MODAIS ==========

  function openModalMovel(ambienteIdx) {
    currentAmbienteIndex = ambienteIdx;
    document.getElementById('movelNome').value = '';
    document.getElementById('modalMovel').style.display = 'block';
    document.getElementById('movelNome').focus();
  }

  function closeModalMovel() {
    document.getElementById('modalMovel').style.display = 'none';
    currentAmbienteIndex = null;
  }

  function openModalPeca(ambienteIdx, movelIdx) {
    currentAmbienteIndex = ambienteIdx;
    currentMovelIndex = movelIdx;
    
    // Limpar formulário
    document.getElementById('tipoPeca').value = '';
    document.getElementById('componentePeca').innerHTML = '<option value="">Selecione...</option>';
    document.getElementById('componentesContainer').style.display = 'none';
    document.getElementById('camposCalculoContainer').innerHTML = '';
    document.getElementById('calculoResultado').style.display = 'none';
    
    document.getElementById('modalPeca').style.display = 'block';
  }

  function closeModalPeca() {
    document.getElementById('modalPeca').style.display = 'none';
    currentAmbienteIndex = null;
    currentMovelIndex = null;
    
    if (currentCalculoTimeout) {
      clearTimeout(currentCalculoTimeout);
      currentCalculoTimeout = null;
    }
  }

  // ========== FUNÇÕES DE IMPRESSÃO ==========

  function imprimirOrcamento() {
    const cliente = document.getElementById('cliente').value || 'Cliente não informado';
    const dataAtual = new Date().toLocaleDateString('pt-BR');
    
    // Calcular totais
    let valorTotal = 0;
    let totalPecasFisicas = 0; // Mudança: contar peças físicas
    
    ambientes.forEach(ambiente => {
      const moveis = ambiente.moveis || [];
      moveis.forEach(movel => {
        const pecas = movel.pecas || [];
        
        pecas.forEach(peca => {
          // Contar quantidade física de peças
          const quantidadeFisica = parseInt(peca.dados_calculo?.quantidade || 1);
          totalPecasFisicas += quantidadeFisica;
          
          if (peca.resultado_calculo && peca.resultado_calculo.custo_total) {
            valorTotal += parseFloat(peca.resultado_calculo.custo_total);
          }
        });
      });
    });

    // Gerar HTML para impressão
    let htmlImpressao = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Orçamento - ${cliente}</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 20px; color: #333; }
          .cabecalho { text-align: center; border-bottom: 2px solid #2563eb; padding-bottom: 10px; margin-bottom: 20px; }
          .titulo { color: #2563eb; margin: 0; }
          .info-basica { display: flex; justify-content: space-between; margin-bottom: 20px; }
          .ambiente { margin-bottom: 20px; border: 1px solid #e5e7eb; border-radius: 8px; }
          .ambiente-header { background: #f9fafb; padding: 12px; border-bottom: 1px solid #e5e7eb; }
          .ambiente-nome { font-weight: bold; color: #1f2937; margin: 0; }
          .movel { margin: 12px; border-left: 3px solid #2563eb; padding-left: 12px; }
          .movel-nome { font-weight: bold; color: #374151; margin-bottom: 8px; }
          .peca { margin: 6px 0; padding: 6px; background: #f9fafb; border-radius: 4px; font-size: 14px; }
          .peca-nome { font-weight: bold; }
          .peca-detalhes { color: #6b7280; margin-top: 2px; }
          .peca-custo { color: #059669; font-weight: bold; margin-top: 2px; }
          .totais { margin-top: 30px; border-top: 2px solid #2563eb; padding-top: 15px; }
          .valor-total { font-size: 24px; font-weight: bold; color: #059669; text-align: right; }
          .resumo-numeros { display: flex; justify-content: space-around; margin: 15px 0; }
          .numero { text-align: center; }
          .numero-valor { font-size: 20px; font-weight: bold; color: #1f2937; }
          .numero-label { color: #6b7280; font-size: 12px; }
          @media print {
            body { margin: 0; }
            .ambiente { page-break-inside: avoid; }
          }
        </style>
      </head>
      <body>
        <div class="cabecalho">
          <h1 class="titulo">ORÇAMENTO DE MARCENARIA</h1>
        </div>
        
        <div class="info-basica">
          <div><strong>Cliente:</strong> ${cliente}</div>
          <div><strong>Data:</strong> ${dataAtual}</div>
        </div>
    `;

    // Adicionar ambientes
    ambientes.forEach(ambiente => {
      const moveis = ambiente.moveis || [];
      let custoAmbiente = 0;
      
      // Calcular custo do ambiente
      moveis.forEach(movel => {
        const pecas = movel.pecas || [];
        pecas.forEach(peca => {
          if (peca.resultado_calculo && peca.resultado_calculo.custo_total) {
            custoAmbiente += parseFloat(peca.resultado_calculo.custo_total);
          }
        });
      });

      htmlImpressao += `
        <div class="ambiente">
          <div class="ambiente-header">
            <h3 class="ambiente-nome">${ambiente.nome} - R$ ${custoAmbiente.toFixed(2)}</h3>
          </div>
      `;

      moveis.forEach(movel => {
        const pecas = movel.pecas || [];
        
        // Calcular total de peças físicas do móvel para impressão
        const totalPecasFisicasMovel = pecas.reduce((acc, peca) => {
          const quantidade = parseInt(peca.dados_calculo?.quantidade || 1);
          return acc + quantidade;
        }, 0);
        
        htmlImpressao += `
          <div class="movel">
            <div class="movel-nome">${movel.nome} (${totalPecasFisicasMovel} peças físicas)</div>
        `;

        pecas.forEach(peca => {
          const custo = peca.resultado_calculo?.custo_total || 0;
          const resumo = peca.resultado_calculo?.resumo || peca.resumo || '';
          const quantidade = parseInt(peca.dados_calculo?.quantidade || 1);
          
          htmlImpressao += `
            <div class="peca">
              <div class="peca-nome">${peca.tipo_nome} - ${peca.componente_nome} (${quantidade}x)</div>
              <div class="peca-detalhes">${resumo}</div>
              <div class="peca-custo">R$ ${custo.toFixed(2)}</div>
            </div>
          `;
        });

        htmlImpressao += `</div>`;
      });

      htmlImpressao += `</div>`;
    });

    // Adicionar totais (usando peças físicas)
    const totalMoveisFinal = ambientes.reduce((acc, amb) => acc + (amb.moveis || []).length, 0);
    
    htmlImpressao += `
        <div class="totais">
          <div class="resumo-numeros">
            <div class="numero">
              <div class="numero-valor">${ambientes.length}</div>
              <div class="numero-label">Ambientes</div>
            </div>
            <div class="numero">
              <div class="numero-valor">${totalMoveisFinal}</div>
              <div class="numero-label">Móveis</div>
            </div>
            <div class="numero">
              <div class="numero-valor">${totalPecasFisicas}</div>
              <div class="numero-label">Peças Físicas</div>
            </div>
          </div>
          <div class="valor-total">TOTAL: R$ ${valorTotal.toFixed(2)}</div>
        </div>
      </body>
      </html>
    `;

    // Abrir nova janela para impressão
    const janelaImpressao = window.open('', '_blank');
    janelaImpressao.document.write(htmlImpressao);
    janelaImpressao.document.close();
    janelaImpressao.focus();
    janelaImpressao.print();
  }

  // ========== FUNÇÕES DE API ==========

  async function carregarComponentes(tipoPecaCodigo) {
    try {
      const response = await fetch(`/marcenaria/api/componentes/${tipoPecaCodigo}/`);
      const data = await response.json();
      
      if (data.sucesso) {
        const select = document.getElementById('componentePeca');
        select.innerHTML = '<option value="">Selecione...</option>';
        
        data.componentes.forEach(comp => {
          const option = document.createElement('option');
          option.value = comp.id;
          option.textContent = `${comp.nome} - ${comp.fornecedor_nome} (R$ ${comp.custo_unitario})`;
          option.dataset.componente = JSON.stringify(comp);
          select.appendChild(option);
        });
        
        document.getElementById('componentesContainer').style.display = 'block';
      } else {
        alert('Erro ao carregar componentes: ' + data.erro);
      }
    } catch (error) {
      console.error('Erro ao carregar componentes:', error);
      alert('Erro ao carregar componentes');
    }
  }

  async function carregarCamposCalculo(tipoPecaCodigo) {
    try {
      const response = await fetch(`/marcenaria/api/campos-calculo/${tipoPecaCodigo}/`);
      const data = await response.json();
      
      if (data.sucesso) {
        const container = document.getElementById('camposCalculoContainer');
        container.innerHTML = '';
        
        data.campos.forEach(campo => {
          const fieldDiv = document.createElement('div');
          fieldDiv.className = 'campo-calculo';
          
          const label = document.createElement('label');
          label.className = 'label';
          label.setAttribute('for', `campo_${campo.name}`);
          label.textContent = campo.label + (campo.required ? ' *' : '');
          
          const input = document.createElement('input');
          input.type = campo.type;
          input.id = `campo_${campo.name}`;
          input.name = campo.name;
          input.className = 'input-field';
          input.required = campo.required || false;
          
          if (campo.min !== undefined) input.min = campo.min;
          if (campo.max !== undefined) input.max = campo.max;
          if (campo.step !== undefined) input.step = campo.step;
          if (campo.placeholder) input.placeholder = campo.placeholder;
          
          // Adicionar evento de cálculo em tempo real
          input.addEventListener('input', () => {
            if (currentCalculoTimeout) {
              clearTimeout(currentCalculoTimeout);
            }
            currentCalculoTimeout = setTimeout(calcularEmTempoReal, 500);
          });
          
          fieldDiv.appendChild(label);
          fieldDiv.appendChild(input);
          
          if (campo.help) {
            const help = document.createElement('div');
            help.className = 'help-text';
            help.textContent = campo.help;
            fieldDiv.appendChild(help);
          }
          
          container.appendChild(fieldDiv);
        });
      } else {
        alert('Erro ao carregar campos: ' + data.erro);
      }
    } catch (error) {
      console.error('Erro ao carregar campos:', error);
      alert('Erro ao carregar campos');
    }
  }

  // ========== EVENT LISTENERS ==========

  // Ambiente
  btn.addEventListener('click', function(e) {
    e.preventDefault();
    addAmbiente();
  });
  
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addAmbiente();
    }
  });

  // Cliques nos botões dos ambientes, móveis e peças
  container.addEventListener('click', (e) => {
    const btn = e.target.closest('button[data-action]');
    if (!btn) return;

    const ambienteIdx = parseInt(btn.getAttribute('data-ambiente'));
    const movelIdx = btn.hasAttribute('data-movel') ? parseInt(btn.getAttribute('data-movel')) : null;
    const pecaIdx = btn.hasAttribute('data-peca') ? parseInt(btn.getAttribute('data-peca')) : null;
    const action = btn.getAttribute('data-action');

    console.log(`Ação: ${action}, Ambiente: ${ambienteIdx}, Móvel: ${movelIdx}, Peça: ${pecaIdx}`);

    switch (action) {
      case 'remove':
        removeAmbiente(ambienteIdx);
        break;
      case 'add-movel':
        openModalMovel(ambienteIdx);
        break;
      case 'remove-movel':
        removeMovel(ambienteIdx, movelIdx);
        break;
      case 'add-peca':
        openModalPeca(ambienteIdx, movelIdx);
        break;
      case 'remove-peca':
        removePeca(ambienteIdx, movelIdx, pecaIdx);
        break;
    }
  });

  // Modal Móvel
  document.getElementById('btnSalvarMovel').addEventListener('click', () => {
    const nome = document.getElementById('movelNome').value.trim();
    if (!nome) {
      alert('Digite o nome do móvel');
      return;
    }
    
    addMovel(currentAmbienteIndex, nome);
    closeModalMovel();
  });

  document.getElementById('btnCancelarMovel').addEventListener('click', closeModalMovel);
  document.getElementById('btnFecharModalMovel').addEventListener('click', closeModalMovel);

  // Modal Peça
  document.getElementById('tipoPeca').addEventListener('change', (e) => {
    const tipoCodigo = e.target.value;
    if (tipoCodigo) {
      carregarComponentes(tipoCodigo);
      carregarCamposCalculo(tipoCodigo);
    } else {
      document.getElementById('componentesContainer').style.display = 'none';
      document.getElementById('camposCalculoContainer').innerHTML = '';
      document.getElementById('calculoResultado').style.display = 'none';
    }
  });

  document.getElementById('componentePeca').addEventListener('change', () => {
    if (currentCalculoTimeout) {
      clearTimeout(currentCalculoTimeout);
    }
    currentCalculoTimeout = setTimeout(calcularEmTempoReal, 300);
  });

  document.getElementById('btnSalvarPeca').addEventListener('click', async () => {
    const tipoPeca = document.getElementById('tipoPeca');
    const componentePeca = document.getElementById('componentePeca');
    
    if (!tipoPeca.value) {
      alert('Selecione o tipo de peça');
      return;
    }
    
    if (!componentePeca.value) {
      alert('Selecione o componente');
      return;
    }

    // Coletar dados dos campos de cálculo
    const dadosCalculo = {};
    const campos = document.querySelectorAll('#camposCalculoContainer input');
    
    for (let campo of campos) {
      if (campo.required && !campo.value.trim()) {
        alert(`O campo "${campo.previousElementSibling.textContent}" é obrigatório`);
        campo.focus();
        return;
      }
      dadosCalculo[campo.name] = campo.value;
    }

    // Preparar dados da peça
    const tipoOption = tipoPeca.options[tipoPeca.selectedIndex];
    const compOption = componentePeca.options[componentePeca.selectedIndex];
    const componenteData = JSON.parse(compOption.dataset.componente);
    
    const dadosPeca = {
      tipo_codigo: tipoPeca.value,
      tipo_nome: tipoOption.textContent,
      componente_id: componentePeca.value,
      componente_nome: componenteData.nome,
      componente_preco_unitario: componenteData.custo_unitario,
      dados_calculo: dadosCalculo,
      resumo: `${tipoOption.textContent} - ${Object.values(dadosCalculo).join(' x ')}`
    };
    
    await addPeca(currentAmbienteIndex, currentMovelIndex, dadosPeca);
    closeModalPeca();
  });

  document.getElementById('btnCancelarPeca').addEventListener('click', closeModalPeca);
  document.getElementById('btnFecharModalPeca').addEventListener('click', closeModalPeca);

  // Botão de impressão
  const btnImprimir = document.getElementById('btnImprimir');
  if (btnImprimir) {
    btnImprimir.addEventListener('click', (e) => {
      e.preventDefault();
      
      if (ambientes.length === 0) {
        alert('Adicione pelo menos um ambiente antes de imprimir');
        return;
      }
      
      imprimirOrcamento();
    });
  }

  // Fechar modais clicando no overlay
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
      if (e.target.closest('#modalMovel')) {
        closeModalMovel();
      } else if (e.target.closest('#modalPeca')) {
        closeModalPeca();
      }
    }
  });

  // ========== INICIALIZAÇÃO ==========
  
  render();
  document.getElementById('cliente').focus();
});