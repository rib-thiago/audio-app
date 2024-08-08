// script.js
document.addEventListener('DOMContentLoaded', function () {
    const modal = document.querySelector('.modal');
    const closeModalButton = document.querySelector('.modal__close');

    if (modal) {
        modal.classList.add('modal--show'); // Mostra o modal quando o DOM é carregado
    }

    if (closeModalButton) {
        closeModalButton.addEventListener('click', function () {
            modal.classList.remove('modal--show'); // Fecha o modal quando o botão de fechar é clicado
        });
    }

    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.classList.remove('modal--show'); // Fecha o modal se o usuário clicar fora da área do modal
        }
    });
});
