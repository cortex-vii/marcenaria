from django.urls import path
from . import views

app_name = 'marcenaria'

urlpatterns = [
    path('orcamentos/create/', views.orcamento_create, name='orcamento_create'),
    path('marcenaria/api/componentes/<str:tipo_peca_codigo>/', views.get_componentes_por_tipo_peca, name='get_componentes_por_tipo_peca'),
    path('marcenaria/api/campos-calculo/<str:tipo_peca_codigo>/', views.get_campos_calculo_peca, name='get_campos_calculo_peca'),
]