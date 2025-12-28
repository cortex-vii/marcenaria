// Funções para requisições AJAX relacionadas ao orçamento

async function apiBuscarComponentes(tipoPecaCodigo) {
  const response = await fetch(`/marcenaria/api/componentes/${tipoPecaCodigo}/`);
  return await response.json();
}

async function apiBuscarCamposCalculo(tipoPecaCodigo) {
  const response = await fetch(`/marcenaria/api/campos-calculo/${tipoPecaCodigo}/`);
  return await response.json();
}

// Outras funções de API podem ser adicionadas aqui
