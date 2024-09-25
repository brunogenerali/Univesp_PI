function enviarWhatsapp(numero, mensagem) {
    // Substitua 'seu_numero' pelo seu número de WhatsApp com o código do país
    window.open(`https://api.whatsapp.com/send?phone=55${numero}&text=${mensagem}`, '_blank')
}

function enviarMensagem(mensagemId, telefone, mensagem) {
    // Aqui você chama a função que envia a mensagem pelo WhatsApp
    enviarWhatsapp(telefone, mensagem);
  
    // Faz a requisição AJAX para atualizar o campo msg_enviada
    fetch(`/atualizar-msg-enviada/${mensagemId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': '{{ csrf_token }}',
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        alert('Mensagem enviada e status atualizado!');
      } else {
        alert('Erro ao atualizar o status: ' + data.message);
      }
    })
    .catch(error => {
      console.error('Erro:', error);
    });
  }
  
document.addEventListener('DOMContentLoaded', function () {
    const deleteLink = document.querySelector('.nav__link--danger');
    deleteLink.addEventListener('click', function (event) {
        if (!confirm('Tem certeza que deseja apagar todos os dados?')) {
            event.preventDefault();
        }
    });
});
