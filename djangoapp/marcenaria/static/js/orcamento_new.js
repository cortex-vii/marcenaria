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
          ${renderPecas(movel.pecas || [])}
        </div>
      </div>
    `).join('');
  }

  function renderPecas(pecas) {
    if (!pecas || pecas.length === 0) {
      return '<div class="empty-pecas">Nenhuma peça adicionada</div>';
    }

    return pecas.map((peca, pecaIdx) => `
      <div class="peca-item">
        <div class="peca-info">
          <div class="peca-nome">${peca.tipo_nome} - ${peca.componente_nome}</div>
          <div class="peca-detalhes">${peca.resumo || 'Detalhes do cálculo'}</div>
        </div>
        <div class="peca-actions">
          <button type="button" class="btn btn-danger btn-xs" 
                  data-peca="${pecaIdx}" 
                  data-action="remove-peca">
            Remover
          </button>
        </div>
      </div>
    `).join('');
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

  function addPeca(ambienteIdx, movelIdx, dadosPeca) {
    if (!ambientes[ambienteIdx].moveis[movelIdx].pecas) {
      ambientes[ambienteIdx].moveis[movelIdx].pecas = [];
    }
    
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
    
    document.getElementById('modalPeca').style.display = 'block';
  }

  function closeModalPeca() {
    document.getElementById('modalPeca').style.display = 'none';
    currentAmbienteIndex = null;
    currentMovelIndex = null;
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
          option.textContent = `${comp.nome} - ${comp.fornecedor_nome}`;
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

  // Cliques nos botões dos ambientes e móveis
  container.addEventListener('click', (e) => {
    const btn = e.target.closest('button[data-action]');
    if (!btn) return;

    const ambienteIdx = parseInt(btn.getAttribute('data-ambiente'));
    const movelIdx = btn.hasAttribute('data-movel') ? parseInt(btn.getAttribute('data-movel')) : null;
    const pecaIdx = btn.hasAttribute('data-peca') ? parseInt(btn.getAttribute('data-peca')) : null;
    const action = btn.getAttribute('data-action');

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
    }
  });

  document.getElementById('btnSalvarPeca').addEventListener('click', () => {
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
      dados_calculo: dadosCalculo,
      resumo: `${tipoOption.textContent} - ${Object.values(dadosCalculo).join(' x ')}`
    };
    
    addPeca(currentAmbienteIndex, currentMovelIndex, dadosPeca);
    closeModalPeca();
  });

  document.getElementById('btnCancelarPeca').addEventListener('click', closeModalPeca);
  document.getElementById('btnFecharModalPeca').addEventListener('click', closeModalPeca);

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