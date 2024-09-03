function enviarWhatsapp(numero, mensagem) {
    // Substitua 'seu_numero' pelo seu número de WhatsApp com o código do país
    window.open(`https://api.whatsapp.com/send?phone=55${numero}&text=${mensagem}`, '_blank')
}

document.addEventListener('DOMContentLoaded', function () {
    const deleteLink = document.querySelector('.nav__link--danger');
    deleteLink.addEventListener('click', function (event) {
        if (!confirm('Tem certeza que deseja apagar todos os dados?')) {
            event.preventDefault();
        }
    });
});
