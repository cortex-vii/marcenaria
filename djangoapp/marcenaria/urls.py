from django.urls import path
from . import views

app_name = 'marcenaria'

urlpatterns = [
    path('orcamentos/create/', views.orcamento_create, name='orcamento_create'),
    path('orcamentos/<int:pk>/edit/', views.orcamento_edit, name='orcamento_edit'),
    path('orcamentos/<int:pk>/delete/', views.orcamento_delete, name='orcamento_delete'),
    # aqui ele pega os componentes disponiveis para o tipo de peça
    path('marcenaria/api/componentes/<str:tipo_peca_codigo>/', views.get_componentes_por_tipo_peca, name='get_componentes_por_tipo_peca'),
    # aqui ele pega os campos necessários para o cálculo da peça
    path('marcenaria/api/campos-calculo/<str:tipo_peca_codigo>/', views.get_campos_calculo_peca, name='get_campos_calculo_peca'),
    # rota para calcular a peça
    path('marcenaria/api/calcular-peca/', views.calcular_peca_api, name='calcular_peca_api'),
    
    
]