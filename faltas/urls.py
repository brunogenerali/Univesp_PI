from django.urls import path
from faltas.views import index

urlpatterns = [
    path('', index)
]
