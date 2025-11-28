window.onload = function () {
  $cruCallback('executarAnimacaoSobreNos', (result, element) => {
    const teste_animation = element.querySelectorAll('.empresas_parceiras');
    const observador = new IntersectionObserver((item) => {
      item.forEach((saida) => {
        if (saida.isIntersecting) {
          saida.target.classList.add('empresas_parceiras_visiveis');
        } else {
          saida.target.classList.remove('empresas_parceiras_visiveis');
        }
      });
    });

    teste_animation.forEach((elemento) => observador.observe(elemento));
  });
};
