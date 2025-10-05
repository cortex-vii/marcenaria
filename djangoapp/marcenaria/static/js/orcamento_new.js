(function () {
  const input = document.getElementById('ambienteNome');
  const btn = document.getElementById('btnAddAmbiente');
  const list = document.getElementById('ambientesLista');
  const hidden = document.getElementById('id_ambientes_json') || document.querySelector('input[name="ambientes_json"]');

  if (!input || !btn || !list || !hidden) return;

  let ambientes = [];

  function render() {
    list.innerHTML = '';
    if (ambientes.length === 0) {
      list.innerHTML = '<div class="help">Nenhum ambiente adicionado ainda.</div>';
    } else {
      ambientes.forEach((a, idx) => {
        const row = document.createElement('div');
        row.className = 'amb-item';
        row.innerHTML = `
          <span>${a.nome}</span>
          <button type="button" class="btn btn-danger" data-idx="${idx}">Remover</button>
        `;
        list.appendChild(row);
      });
    }
    hidden.value = JSON.stringify(ambientes);
  }

  function addAmbiente() {
    const nome = (input.value || '').trim();
    if (!nome) return;
    ambientes.push({ nome });
    input.value = '';
    input.focus();
    render();
  }

  btn.addEventListener('click', addAmbiente);
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addAmbiente();
    }
  });

  list.addEventListener('click', (e) => {
    const b = e.target.closest('button[data-idx]');
    if (!b) return;
    const idx = parseInt(b.getAttribute('data-idx'), 10);
    ambientes.splice(idx, 1);
    render();
  });

  render();
})();