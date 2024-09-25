from django.urls import path
from faltas.views import (
    index,
    processar_upload,
    add_alunos,
    clear_tables,
    confirm_clear_tables,
    atualizar_msg_enviada,
    cadastrar_alunos,
    faltas_view,
    sucesso_view,
)

urlpatterns = [
    path("", index, name="index"),
    path("upload/", processar_upload, name="upload"),
    path("upload/", faltas_view, name="faltas"),
    path("sucesso/", sucesso_view, name="sucesso"),
    path("cadastro/", add_alunos, name="cadastro"),
    path("clear_tables/", clear_tables, name="clear_tables"),
    path("confirm_clear_tables/", confirm_clear_tables, name="confirm_clear_tables"),
    path("cadastrar-alunos/", cadastrar_alunos, name="cadastrar_alunos"),
    path(
        "atualizar-msg-enviada/<int:mensagem_id>/",
        atualizar_msg_enviada,
        name="atualizar_msg_enviada",
    ),
]
