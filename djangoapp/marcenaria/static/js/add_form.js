/* filepath: s:\01 - Cortex\Produtos\marcenaria-cortex\djangoapp\marcenaria\static\js\add_form.js */
document.addEventListener('DOMContentLoaded', function() {
    
    // Adicionar ícones aos títulos dos fieldsets
    const fieldsetTitles = document.querySelectorAll('.module h2');
    fieldsetTitles.forEach((title, index) => {
        const icons = ['📋', '📝', '⏰'];
        if (icons[index]) {
            title.innerHTML = `${icons[index]} ${title.innerHTML}`;
        }
    });

    // Validação básica para o campo cliente
    const clienteField = document.querySelector('#id_cliente');
    if (clienteField) {
        clienteField.addEventListener('blur', function() {
            const value = this.value.trim();
            
            if (value.length < 2) {
                this.style.borderColor = '#dc3545';
            } else {
                this.style.borderColor = '#28a745';
            }
        });
        
        clienteField.addEventListener('focus', function() {
            this.style.borderColor = '#667eea';
        });
    }

    // Contador de caracteres para descrição
    const descricaoField = document.querySelector('#id_descricao');
    if (descricaoField) {
        const maxLength = 500;
        
        const counter = document.createElement('div');
        counter.style.cssText = `
            font-size: 12px;
            color: #6c757d;
            text-align: right;
            margin-top: 5px;
        `;
        
        const updateCounter = () => {
            const length = descricaoField.value.length;
            counter.textContent = `${length}/${maxLength} caracteres`;
            
            if (length > maxLength * 0.9) {
                counter.style.color = '#dc3545';
            } else if (length > maxLength * 0.7) {
                counter.style.color = '#ffc107';
            } else {
                counter.style.color = '#6c757d';
            }
        };
        
        descricaoField.parentNode.appendChild(counter);
        descricaoField.addEventListener('input', updateCounter);
        updateCounter();
    }

    // Atalho Ctrl+S para salvar
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            const saveButton = document.querySelector('input[name="_save"]');
            if (saveButton) {
                saveButton.click();
            }
        }
    });

    // Confirmação antes de sair com alterações
    let formChanged = false;
    const formInputs = document.querySelectorAll('input, select, textarea');
    
    formInputs.forEach(input => {
        input.addEventListener('change', () => {
            formChanged = true;
        });
    });

    window.addEventListener('beforeunload', (e) => {
        if (formChanged) {
            e.preventDefault();
            e.returnValue = 'Você tem alterações não salvas. Deseja sair?';
        }
    });

    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', () => {
            formChanged = false;
        });
    }

    // Função para adicionar novos inlines
    window.addAnotherInline = function(prefix) {
        const totalForms = document.querySelector(`#id_${prefix}-TOTAL_FORMS`);
        const formCount = parseInt(totalForms.value);
        
        // Clone o último formulário
        const lastForm = document.querySelector(`.ambiente-inline:last-child`);
        if (lastForm) {
            const newForm = lastForm.cloneNode(true);
            
            // Limpar valores dos campos
            const inputs = newForm.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                if (input.type !== 'hidden') {
                    input.value = '';
                }
                // Atualizar IDs e names
                const oldId = input.id;
                const oldName = input.name;
                if (oldId) {
                    input.id = oldId.replace(/-\d+-/, `-${formCount}-`);
                }
                if (oldName) {
                    input.name = oldName.replace(/-\d+-/, `-${formCount}-`);
                }
            });
            
            // Atualizar título
            const title = newForm.querySelector('h3');
            if (title) {
                title.textContent = 'Novo Ambiente';
            }
            
            // Inserir o novo formulário
            lastForm.parentNode.insertBefore(newForm, lastForm.nextSibling);
            
            // Atualizar contador
            totalForms.value = formCount + 1;
        }
    };
    
    // Validação para ambientes
    const ambienteInputs = document.querySelectorAll('[id*="ambiente"][id*="nome"]');
    ambienteInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value.trim() === '') {
                this.style.borderColor = '#dc3545';
            } else {
                this.style.borderColor = '#28a745';
            }
        });
    });

    (function () {
      const input = document.getElementById('ambienteNome');
      const btn = document.getElementById('btnAddAmbiente');
      const list = document.getElementById('ambientesLista');
      const hidden = document.getElementById('ambientesJson');

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
        const btn = e.target.closest('button[data-idx]');
        if (!btn) return;
        const idx = parseInt(btn.getAttribute('data-idx'), 10);
        ambientes.splice(idx, 1);
        render();
      });

      render();
    })();
});