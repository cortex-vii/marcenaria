from django.urls import path
from . import views

app_name = 'marcenaria'

urlpatterns = [
    path('orcamentos/create/', views.orcamento_create, name='orcamento_create'),
]