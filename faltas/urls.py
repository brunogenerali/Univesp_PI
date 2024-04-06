from django.urls import path
from faltas.views import index, processar_upload

urlpatterns = [
    path('', index, name='index'),
    path("upload/", processar_upload, name="upload"),
]
