from django.urls import path    
from .views import *



urlpatterns = [
    path("", index, name="index_industria"),
    path("saida_produto/", saida_produto, name="saida_produto"),# type: ignore
    path("ordem_producao/", ordem_producao, name="ordem_producao"),# type: ignore
    path("ordem_producao/create/", create_ordem_producao, name="create_ordem_producao"),# type: ignore
    path("ordem_producao/read/<int:id>/", read_ordem_producao, name="read_ordem_producao"),# type: ignore
    path("ordem_producao/update/<int:id>/", update_ordem_producao, name="update_ordem_producao"),# type: ignore
    path("ordem_producao/delete/<int:id>/", delete_ordem_producao, name="delete_ordem_producao"),# type: ignore
    path('saida_produto/create/', create_saida_produto, name='create_saida_produto'), # type: ignore
    path('saida_produto/read/<int:id>/', read_saida_produto, name='read_saida_produto'),# type: ignore
    path('saida_produto/update/<int:id>/', update_saida_produto, name='update_saida_produto'), # type: ignore
    path('saida_produto/delete/<int:id>/', delete_saida_produto, name='delete_saida_produto'),# type: ignore
    path('entrada_produto/', entrada_produto, name='entrada_produto'),# type: ignore
    path('entrada_produto/create/', create_entrada_produto, name='create_entrada_produto'), # type: ignore
    path('entrada_produto/read/<int:id>/', read_entrada_produto, name='read_entrada_produto'),# type: ignore
    path('entrada_produto/update/<int:id>/', update_entrada_produto, name='update_entrada_produto'), # type: ignore
    path('entrada_produto/delete/<int:id>/', delete_entrada_produto, name='delete_entrada_produto'),# type: ignore
    path('produto/', produto, name='produto'),
    path('produto/create/', create_produto, name='create_produto'),# type: ignore
    path('produto/read/<int:id>/', read_produto, name='read_produto'),# type: ignore    
    path('produto/update/<int:id>/', update_produto, name='update_produto'),# type: ignore
    path('produto/delete/<int:id>/', delete_produto, name='delete_produto'),# type: ignore
    path('materia_prima/', materia_prima, name='materia_prima'),
    path('materia_prima/create/', create_materia_prima, name='create_materia_prima'),# type: ignore
    path('materia_prima/read/<int:id>/', read_materia_prima, name='read_materia_prima'),# type: ignore
    path('materia_prima/update/<int:id>/', update_materia_prima, name='update_materia_prima'),# type: ignore
    path('materia_prima/delete/<int:id>/', delete_materia_prima, name='delete_materia_prima'),# type: ignore
    path('custo/', custo, name='custo'),




    path('custo_receita/<int:id>/', custo_receita, name='custo_receita'),
    path('ingrediente/<int:id>/', ingrediente, name='ingrediente'),
    path('embalagem/<int:id>/', embalagem, name='embalagem'),
    path('producao_funcionario/<int:id>/', producao_funcionario, name='producao_funcionario'),
    
]