document.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('ambienteNome');
  const btn = document.getElementById('btnAddAmbiente');
  const container = document.getElementById('ambientesContainer');  // MUDANÇA AQUI
  const hidden = document.getElementById('ambientesJson');

  if (!input || !btn || !container || !hidden) {
    console.error('Um ou mais elementos do formulário de ambientes não foram encontrados.');
    console.error('Input:', input);
    console.error('Botão:', btn);
    console.error('Container:', container);
    console.error('Hidden:', hidden);
    return;
  }

  let ambientes = [];
  try {
    ambientes = JSON.parse(hidden.value || '[]');
  } catch (e) {
    console.error('Erro ao carregar ambientes do campo hidden:', e);
    ambientes = [];
  }

  function render() {
    container.innerHTML = '';  // MUDANÇA AQUI
    
    if (ambientes.length === 0) {
      container.innerHTML = '<div class="empty-state">Nenhum ambiente adicionado</div>';
    } else {
      ambientes.forEach((ambiente, idx) => {
        const ambienteDiv = document.createElement('div');
        ambienteDiv.className = 'ambiente-item';
        ambienteDiv.innerHTML = `
          <div class="ambiente-header">
            <h3>${ambiente.nome}</h3>
            <div class="ambiente-actions">
              <button type="button" class="btn btn-primary btn-sm" data-ambiente="${idx}" data-action="add-movel">
                Adicionar Móvel
              </button>
              <button type="button" class="btn btn-danger btn-sm" data-ambiente="${idx}" data-action="remove">
                Remover Ambiente
              </button>
            </div>
          </div>
          <div class="moveis-container" id="moveis-${idx}">
            <div class="empty-moveis">Nenhum móvel adicionado</div>
          </div>
        `;
        container.appendChild(ambienteDiv);
      });
    }
    
    hidden.value = JSON.stringify(ambientes);
  }

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

  // --- Event Listeners ---
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

  container.addEventListener('click', (e) => {
    const btn = e.target.closest('button[data-action]');
    if (!btn) return;

    const ambienteIdx = parseInt(btn.getAttribute('data-ambiente'));
    const action = btn.getAttribute('data-action');

    if (action === 'remove') {
      removeAmbiente(ambienteIdx);
    } else if (action === 'add-movel') {
      // TODO: Abrir modal para adicionar móvel
      alert(`Adicionar móvel ao ambiente: ${ambientes[ambienteIdx].nome}`);
    }
  });

  // Renderizar estado inicial
  render();
  
  // Focar no campo cliente ao carregar
  document.getElementById('cliente').focus();
});