from django.urls import path
from faltas.views import index, processar_upload, add_alunos, clear_tables, confirm_clear_tables

urlpatterns = [
    path('', index, name='index'),
    path("upload/", processar_upload, name="upload"),     
    path('cadastro/', add_alunos, name="cadastro" ),
    path('clear_tables/', clear_tables, name='clear_tables'),
    path('confirm_clear_tables/', confirm_clear_tables, name='confirm_clear_tables'),
]
