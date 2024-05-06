from django.urls import path
from faltas.views import index, processar_upload, add_alunos, upload

urlpatterns = [
    path('', index, name='index'),
    path("upload/", processar_upload, name="upload"), 
    #path("upload/", upload, name="upload"), 
    path('cadastro/', add_alunos, name="cadastro" ),
]
