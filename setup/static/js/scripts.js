function enviarWhatsapp(numero, mensagem) {
    // Substitua 'seu_numero' pelo seu número de WhatsApp com o código do país
    window.open(`https://api.whatsapp.com/send?phone=55${numero}&text=${mensagem}`, '_blank')
}

function enviarMensagem(mensagemId, telefone, mensagem) {
    // Aqui você chama a função que envia a mensagem pelo WhatsApp
    enviarWhatsapp(telefone, mensagem);

    const csrftoken = getCSRFToken();

    fetch(`/atualizar-msg-enviada/${mensagemId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Mensagem enviada e status atualizado!');
                location.reload(true);
            } else {
                alert('Erro ao atualizar o status: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        });
}
