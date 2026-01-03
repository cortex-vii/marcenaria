document.addEventListener('DOMContentLoaded', function () {
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

  // ========== FUNÇÕES DE UTILITÁRIO ==========

  function toggleDetalhesCalculo(button) {
    const pecaItem = button.closest('.peca-item');
    const detalhes = pecaItem.querySelector('.peca-detalhes-expandidos');
    const isExpandida = pecaItem.getAttribute('data-peca-expandida') === 'true';

    if (isExpandida) {
      detalhes.style.display = 'none';
      pecaItem.setAttribute('data-peca-expandida', 'false');
      button.textContent = '📊';
      button.title = 'Ver detalhes';
    } else {
      detalhes.style.display = 'block';
      pecaItem.setAttribute('data-peca-expandida', 'true');
      button.textContent = '📈';
      button.title = 'Ocultar detalhes';
    }
  }

  // Tornar a função global para uso no HTML
  window.toggleDetalhesCalculo = toggleDetalhesCalculo;

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

    return moveis.map((movel, movelIdx) => {
      const totalPecasFisicas = (movel.pecas || []).reduce((acc, peca) => {
        const quantidade = parseInt(peca.dados_calculo?.quantidade || 1);
        return acc + quantidade;
      }, 0);

      return `
        <div class="movel-item">
          <div class="movel-header">
            <h4>
              ${movel.nome}
              ${totalPecasFisicas > 0 ? `<span class="movel-contador-pecas">${totalPecasFisicas}</span>` : ''}
            </h4>
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
      `;
    }).join('');
  }

  function renderPecas(pecas, ambienteIdx, movelIdx) {
    if (!pecas || pecas.length === 0) {
      return '<div class="empty-pecas">Nenhuma peça adicionada</div>';
    }

    // Função para obter ícone do tipo de peça
    function getTipoPecaIcon(tipoCodigo) {
      const icons = {
        'PC-004': { icon: '📄', class: 'fundo' },     // Fundo simples
        'PC-009': { icon: '📱', class: 'lateral' },   // Lateral simples
        'PC-006': { icon: '📱', class: 'lateral' },   // Lateral dupla
        'PC-002': { icon: '📋', class: 'base' },      // Base simples
        'PC-001': { icon: '📋', class: 'base' },      // Base dupla
        'PC-005': { icon: '🗂️', class: 'gaveta' },    // Gaveta
        'PC-010': { icon: '🚪', class: 'porta' },     // Porta de abrir
        'PC-011': { icon: '🚪', class: 'porta' },     // Porta de correr
      };
      return icons[tipoCodigo] || { icon: '🔧', class: 'base' };
    }

    const listHeader = `
      <div class="pecas-lista">
        <div class="pecas-lista-header">
          <div>Peça / Componente</div>
          <div>Quantidade</div>
          <div>Valor</div>
          <div>Ação</div>
        </div>
    `;

    const listItems = pecas.map((peca, pecaIdx) => {
      const iconInfo = getTipoPecaIcon(peca.tipo_codigo);
      const quantidade = parseInt(peca.dados_calculo?.quantidade || 1);
      const custo = peca.resultado_calculo?.custo_total || 0;
      const resumoCalculo = peca.resultado_calculo?.resumo || '';

      // Detalhes expandidos do cálculo
      const detalhesExpandidos = peca.resultado_calculo ? `
        <div class="peca-detalhes-expandidos">
          <div class="peca-calculo-detalhado">
            ${peca.resultado_calculo.area_por_peca ? `
              <div class="calculo-item">
                <span class="calculo-label">Área por peça:</span>
                <span class="calculo-valor">${peca.resultado_calculo.area_por_peca.toFixed(4)} m²</span>
              </div>
            ` : ''}
            ${peca.resultado_calculo.area_total ? `
              <div class="calculo-item">
                <span class="calculo-label">Área total:</span>
                <span class="calculo-valor">${peca.resultado_calculo.area_total.toFixed(4)} m²</span>
              </div>
            ` : ''}
            ${peca.resultado_calculo.quantidade_utilizada ? `
              <div class="calculo-item">
                <span class="calculo-label">Material usado:</span>
                <span class="calculo-valor">${peca.resultado_calculo.quantidade_utilizada.toFixed(4)} ${peca.resultado_calculo.unidade || 'm²'}</span>
              </div>
            ` : ''}
            <div class="calculo-item">
              <span class="calculo-label">Resumo:</span>
              <span class="calculo-valor">${resumoCalculo}</span>
            </div>
          </div>
        </div>
      ` : '';

      return `
        <div class="peca-item" data-peca-expandida="false">
          <div class="peca-info">
            <div class="peca-nome">
              <span class="tipo-peca-icon ${iconInfo.class}">${iconInfo.icon}</span>
              ${peca.tipo_nome}
            </div>
            <div class="peca-componente">
              ${peca.componente_nome}
            </div>
          </div>
          <div class="peca-quantidade-col">
            <span class="badge badge-primary">${quantidade}x</span>
          </div>
          <div class="peca-valor-col">
            R$ ${custo.toFixed(2)}
          </div>
          <div class="peca-actions">
            <button type="button" class="btn btn-secondary btn-xs" 
                    title="Ver detalhes"
                    onclick="toggleDetalhesCalculo(this)">
              📊
            </button>
            <button type="button" class="btn btn-danger btn-xs" 
                    data-ambiente="${ambienteIdx}"
                    data-movel="${movelIdx}"
                    data-peca="${pecaIdx}" 
                    data-action="remove-peca"
                    title="Remover peça">
              🗑️
            </button>
          </div>
          ${detalhesExpandidos}
        </div>
      `;
    }).join('');

    return listHeader + listItems + '</div>';
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
      let totalPecasAmbiente = 0;

      moveis.forEach(movel => {
        const pecas = movel.pecas || [];

        pecas.forEach(peca => {
          // Contar peças físicas
          const quantidadeFisica = parseInt(peca.dados_calculo?.quantidade || 1);
          totalPecasAmbiente += quantidadeFisica;

          if (peca.resultado_calculo && peca.resultado_calculo.custo_total) {
            custoAmbiente += parseFloat(peca.resultado_calculo.custo_total);
          }
        });
      });

      const percentualDoTotal = ambientes.reduce((total, amb) => {
        const ambMoveis = amb.moveis || [];
        let ambCusto = 0;
        ambMoveis.forEach(movel => {
          const pecas = movel.pecas || [];
          pecas.forEach(peca => {
            if (peca.resultado_calculo && peca.resultado_calculo.custo_total) {
              ambCusto += parseFloat(peca.resultado_calculo.custo_total);
            }
          });
        });
        return total + ambCusto;
      }, 0);

      const percentual = percentualDoTotal > 0 ? (custoAmbiente / percentualDoTotal * 100) : 0;

      html += `
        <div class="ambiente-resumo">
          <div class="ambiente-resumo-nome">
            🏠 ${ambiente.nome}
            <span class="badge badge-success">R$ ${custoAmbiente.toFixed(2)}</span>
            ${percentual > 0 ? `<span class="badge badge-primary">${percentual.toFixed(1)}%</span>` : ''}
          </div>
          <div style="margin-top: 6px;">
            ${moveis.map(movel => {
        const qtdPecasFisicas = (movel.pecas || []).reduce((acc, peca) => {
          return acc + parseInt(peca.dados_calculo?.quantidade || 1);
        }, 0);

        let custoMovel = 0;
        (movel.pecas || []).forEach(peca => {
          if (peca.resultado_calculo && peca.resultado_calculo.custo_total) {
            custoMovel += parseFloat(peca.resultado_calculo.custo_total);
          }
        });

        return `
                <div class="movel-resumo">
                  📦 ${movel.nome} 
                  <span class="badge badge-warning">${qtdPecasFisicas} peças</span>
                  <span style="color: #059669; font-weight: 600; font-size: 11px;">R$ ${custoMovel.toFixed(2)}</span>
                </div>
              `;
      }).join('')}
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  }

  // ========== FUNÇÕES DE CÁLCULO ==========

  async function calcularPeca(tipoPecaCodigo, dadosCalculo, componenteData, componentesAdicionais = {}) {
    try {
      const response = await fetch('/marcenaria/api/calcular-peca/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({
          tipo_peca_codigo: tipoPecaCodigo,
          dados_calculo: dadosCalculo,
          componente_id: componenteData.id,
          componentes_adicionais: componentesAdicionais // <-- Adicionado aqui
        })
      });

      if (response.ok) {
        return await response.json();
      } else {
        // Fallback: cálculo simples no frontend
        return { sucesso: false, erro: 'Erro ao calcular a peça. Tente novamente mais tarde.' };
      }
    } catch (error) {
      return { sucesso: false, erro: 'Erro ao calcular a peça. Tente novamente mais tarde.' };
    }
  }

function mostrarResultadoCalculo(resultado) {
    const container = document.getElementById('calculoResultado');
    const detalhes = document.getElementById('calculoDetalhes');
    const custo = document.getElementById('calculoCusto');

    if (resultado.sucesso) {
        container.className = 'calculo-resultado calculo-sucesso';

        let html = `
            <div>Área por peça: ${resultado.area_por_peca?.toFixed(4) || 0} m²</div>
            <div>Área total: ${resultado.area_total?.toFixed(4) || 0} m²</div>
            <div>${resultado.resumo || ''}</div>
            <hr>
            <div><strong>Detalhamento dos componentes:</strong></div>
            <ul style="margin:0;padding-left:18px">
        `;
        if (Array.isArray(resultado.detalhes)) {
            resultado.detalhes.forEach(item => {
                html += `<li>
                    <strong>${item.componente || ''}</strong>
                    ${item.tipo ? `(${item.tipo})` : ''}
                    ${item.quantidade !== undefined ? `: ${item.quantidade.toFixed(2)} ${item.unidade || ''}` : ''}
                    ${item.quantidade_utilizada !== undefined ? `: ${item.quantidade_utilizada.toFixed(2)} ${item.unidade || ''}` : ''}
                    - <b>R$ ${(item.custo || item.custo_total || 0).toFixed(2)}</b>
                    <br><span style="color: #888">${item.resumo || ''}</span>
                </li>`;
            });
        }
        html += '</ul>';

        detalhes.innerHTML = html;
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

      // Coletar componentes adicionais selecionados (enviar apenas o id)
      const adicionaisSelecionados = [];
      const adicionaisContainer = document.getElementById('componentesAdicionaisContainer');
      const selectsAdicionais = adicionaisContainer.querySelectorAll('select');
      for (let select of selectsAdicionais) {
        if (select.required && !select.value) {
          alert('Selecione todos os componentes adicionais obrigatórios');
          return;
        }
        adicionaisSelecionados.push(select.value);
      }

    // Fazer cálculo
    const resultado = await calcularPeca(tipoPeca, dadosCalculo, componenteData, adicionaisSelecionados);
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
      console.log(" componentes disponíveis :", data);


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

  async function carregarComponentesAdicionais(tipoPecaCodigo) {
    try {
      const response = await fetch(`/marcenaria/api/componentes/${tipoPecaCodigo}/`);
      const data = await response.json();

      if (data.sucesso && data.componentes_adicionais) {
        const adicionaisContainer = document.getElementById('componentesAdicionaisContainer');
        adicionaisContainer.innerHTML = '';

        Object.values(data.componentes_adicionais).forEach(grupo => {
          // Título do grupo (nome do componente)
          const label = document.createElement('label');
          label.className = 'label';
          label.textContent = grupo.nome + ' *';

          // Select dos componentes adicionais
          const select = document.createElement('select');
          select.className = 'input-field';
          select.id = `componenteAdicional_${grupo.codigo}`;
          select.name = `componenteAdicional_${grupo.codigo}`;
          select.required = true;

          select.innerHTML = '<option value="">Selecione...</option>';
          grupo.componentes.forEach(comp => {
            const option = document.createElement('option');
            option.value = comp.id;
            option.textContent = `${comp.nome} (R$ ${comp.custo_unitario})`;
            option.dataset.componente = JSON.stringify(comp);
            select.appendChild(option);
          });

          // Adicionar ao container
          adicionaisContainer.appendChild(label);
          adicionaisContainer.appendChild(select);

          // Evento para cálculo em tempo real se necessário
          select.addEventListener('change', () => {
            if (currentCalculoTimeout) clearTimeout(currentCalculoTimeout);
            currentCalculoTimeout = setTimeout(calcularEmTempoReal, 300);
          });
        });

        adicionaisContainer.style.display = 'block';
      } else {
        document.getElementById('componentesAdicionaisContainer').style.display = 'none';
      }
    } catch (error) {
      console.error('Erro ao carregar componentes adicionais:', error);
      alert('Erro ao carregar componentes adicionais');
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
  btn.addEventListener('click', function (e) {
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
      carregarComponentesAdicionais(tipoCodigo);
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

    // Coletar componentes adicionais selecionados
    const adicionaisSelecionados = [];
    const adicionaisContainer = document.getElementById('componentesAdicionaisContainer');
    const selectsAdicionais = adicionaisContainer.querySelectorAll('select');
    for (let select of selectsAdicionais) {
      if (select.required && !select.value) {
        alert('Selecione todos os componentes adicionais obrigatórios');
        return;
      }
        adicionaisSelecionados.push(select.value);
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
      componentes_adicionais: adicionaisSelecionados, // Agora é um array de objetos
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