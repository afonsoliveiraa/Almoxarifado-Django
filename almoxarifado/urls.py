from django.urls import path

from almoxarifado.views import index, produto, produto_delete, entrada, entrada_delete, entrada_createPage, \
    entrada_create, entrada_edit, item_create, item_delete, saida, saida_createPage, saida_edit, saida_create, \
    saida_delete, itemSaida_create, itemSaida_delete, produto_createPage, produto_create, entrada_update, saida_update, \
    estoque, estoque_day, register

urlpatterns = [
    path('', index, name='index'),

    path('register/', register, name='register'),

    path('produto/', produto, name='produto'),
    path('produto_createPage/', produto_createPage, name='produto_createPage'),
    path('produto_create/', produto_create, name='produto_create'),
    path('produto_delete/<int:id>', produto_delete, name='produto_delete'),

    path('entrada/', entrada, name='entrada'),
    path('entrada_createPage/', entrada_createPage, name='entrada_createPage'),
    path('entrada_create/', entrada_create, name='entrada_create'),
    path('entrada_edit/<int:entrada_id>/', entrada_edit, name='entrada_edit'),
    path('entrada_update/<int:id>/', entrada_update, name='entrada_update'),
    path('item_create/<int:entrada_id>/', item_create, name='item_create'),
    path('item_delete/<int:id>/', item_delete, name='item_delete'),
    path('entrada_delete/<int:id>', entrada_delete, name='entrada_delete'),

    path('saida/', saida, name='saida'),
    path('saida_createPage/', saida_createPage, name='saida_createPage'),
    path('saida_edit/<int:saida_id>/', saida_edit, name='saida_edit'),
    path('saida_update/<int:id>/', saida_update, name='saida_update'),
    path('saida_create/', saida_create, name='saida_create'),
    path('itemSaida_create/<int:saida_id>/', itemSaida_create, name='itemSaida_create'),
    path('itemSaida_delete/<int:id>/', itemSaida_delete, name='itemSaida_delete'),
    path('saida_delete/<int:id>', saida_delete, name='saida_delete'),

    path('estoque/', estoque, name='estoque'),
    path('estoque_day/', estoque_day, name='estoque_day'),

]
