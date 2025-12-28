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