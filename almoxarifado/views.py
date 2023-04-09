from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.utils import timezone

from almoxarifado.admin import CustomUserCreationForm
from almoxarifado.forms import EntradaForm, Item_EntradaForm, SaidaForm, Item_SaidaForm, ProdutoForm
from almoxarifado.models import Produto, Entrada, Item_Entrada, Saida, Item_Saida


# Create your views here.


def register(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_valid = False
            user.save()
            messages.success(request, 'Registrado. Agora faça o login para começar!')
            return redirect('index')

        else:
            print('invalid registration details')

    return render(request, "registration/register.html", {"form": form})


@login_required
def index(request):
    data_atual = datetime.now(tz=timezone.utc)
    produtos_hoje = Produto.objects.filter(data=data_atual).count()

    y = 0
    entradas = Entrada.objects.filter(date_create=data_atual)
    for entrada in entradas:
        itens_entrada = Item_Entrada.objects.filter(entrada=entrada)
        for item in itens_entrada:
            x = item.amount_produto * item.price_produto
            y += x

    w = 0
    ano_atual = data_atual.year
    mes_atual = data_atual.month

    entradas_mes = Entrada.objects.filter(date_create__year=ano_atual, date_create__month=mes_atual)

    for entrada in entradas_mes:
        itens_entrada = Item_Entrada.objects.filter(entrada=entrada)
        for item in itens_entrada:
            x = item.amount_produto * item.price_produto
            w += x
    context = {
        'produtos_hoje': produtos_hoje,
        'data_atual': data_atual,
        'y': y,
        'w': w,
    }
    return render(request, 'interface/index/index.html', context)


# Produtos

@login_required
def produto(request):
    produtos = Produto.objects.all()

    context = {
        'produtos': produtos,
    }
    return render(request, 'interface/produto/produto_page.html', context)


@login_required
def produto_createPage(request):
    form = ProdutoForm()

    context = {
        'form': form,
    }
    return render(request, 'interface/produto/produto_createPage.html', context)


@login_required
def produto_create(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(produto)
    else:
        form = ProdutoForm()

    context = {
        'form': form,
    }
    return render(request, 'interface/produto/produto_createPage.html', context)


@login_required
def produto_delete(request, id):
    produto_obj = Produto.objects.get(id=id)

    if produto_obj.produto_item.exists():
        return HttpResponseNotFound('<h1>Produto utilizado em alguma entrada</h1>')
    else:
        produto_obj.delete()
        return redirect(produto)


# Entradas

@login_required
def entrada(request):
    entradas = Entrada.objects.all()

    context = {
        'entradas': entradas,
    }
    return render(request, 'interface/entrada/entrada_page.html', context)


@login_required
def entrada_createPage(request):
    form = EntradaForm()

    context = {
        'form': form,
    }
    return render(request, 'interface/entrada/entrada_createPage.html', context)


@login_required
def entrada_create(request):
    if request.method == 'POST':
        form = EntradaForm(request.POST)

        if form.is_valid():
            entrada_obj = form.save()
            entrada_obj.save()
            return redirect('entrada_edit', entrada_id=entrada_obj.id)
    else:
        form = EntradaForm()
    context = {
        'form': form,
    }
    return render(request, 'interface/entrada/entrada_createPage.html', context)


@login_required
def entrada_edit(request, entrada_id):
    entrada_obj = Entrada.objects.get(id=entrada_id)

    form = EntradaForm(instance=entrada_obj)
    item_form = Item_EntradaForm()

    itens = Item_Entrada.objects.filter(entrada=entrada_obj)

    total_itens = 0
    for item in itens:
        x = item.amount_produto * item.price_produto
        total_itens += x

    context = {
        'form': form,
        'item_form': item_form,
        'entrada': entrada_obj,
        'itens': itens,
        'total_itens': total_itens,
    }
    return render(request, 'interface/entrada/entrada_edit.html', context)


@login_required
def entrada_update(request, id):
    entrada_obj = Entrada.objects.get(id=id)

    if request.method == 'POST':
        form = EntradaForm(request.POST, instance=entrada_obj)

        if form.is_valid():

            if not entrada_obj.entrada_item.exists():
                form.save()
                return redirect('entrada_edit', entrada_id=entrada_obj.id)
            else:
                return HttpResponseNotFound('<h1>Entrada com itens, para alterar exclua os itens primeiro</h1>')
    else:
        form = EntradaForm()

    context = {
        'form': form,
    }
    return render(request, 'interface/entrada/entrada_edit.html', context)


@login_required
def entrada_delete(request, id):
    entrada_obj = Entrada.objects.get(id=id)

    if entrada_obj.entrada_item.exists():
        return HttpResponseNotFound('<h1>Entrada com itens</h1>')
    else:
        entrada_obj.delete()
        return redirect(entrada)


# Itens Entrada

@login_required
def item_create(request, entrada_id):
    entrada_obj = Entrada.objects.get(id=entrada_id)

    if request.method == 'POST':
        item_form = Item_EntradaForm(request.POST)

        if item_form.is_valid():
            items_entrada = Item_Entrada.objects.filter(entrada=entrada_obj)

            item = item_form.save(commit=False)
            item.entrada = entrada_obj

            y = 0

            for item_obj in items_entrada:
                x = item_obj.amount_produto * item_obj.price_produto
                y += x

            y += item.amount_produto * item.price_produto

            if y <= entrada_obj.total:
                item.save()

                produto_obj = Produto.objects.get(id=item.produto_entrada.id)
                produto_obj.estoque += item.amount_produto
                produto_obj.data = entrada_obj.date_create
                produto_obj.save()

                return redirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseNotFound('<h1>Total dos itens superior ao da entrada</h1>')
    else:
        item_form = Item_EntradaForm()
    context = {
        'item_form': item_form,
    }
    return render(request, 'interface/entrada/entrada_page.html', context)


@login_required
def item_delete(request, id):
    item_obj = Item_Entrada.objects.get(id=id)
    item_obj.delete()

    produto_obj = Produto.objects.get(id=item_obj.produto_entrada.id)
    produto_obj.estoque -= item_obj.amount_produto
    produto_obj.data = produto_obj.data_anterior
    produto_obj.save()

    return redirect(request.META.get('HTTP_REFERER'))


# Saídas

@login_required
def saida(request):
    saidas = Saida.objects.all()

    context = {
        'saidas': saidas,
    }
    return render(request, 'interface/saida/saida_page.html', context)


@login_required
def saida_createPage(request):
    form = SaidaForm()

    context = {
        'form': form,
    }
    return render(request, 'interface/saida/saida_createPage.html', context)


@login_required
def saida_create(request):
    if request.method == 'POST':
        form = SaidaForm(request.POST)

        if form.is_valid():
            saida = form.save()
            saida.save()
            return redirect('saida_edit', saida_id=saida.id)
    else:
        form = SaidaForm()
    context = {
        'form': form,
    }
    return render(request, 'interface/saida/saida_createPage.html', context)


@login_required
def saida_edit(request, saida_id):
    saida_obj = Saida.objects.get(id=saida_id)
    form = SaidaForm(instance=saida_obj)

    itens_saida = Item_Saida.objects.filter(saida=saida_obj)
    item_form = Item_SaidaForm()

    context = {
        'form': form,
        'itens_saida': itens_saida,
        'item_form': item_form,
        'saida': saida_obj,
    }
    return render(request, 'interface/saida/saida_edit.html', context)


@login_required
def saida_update(request, id):
    saida_obj = Saida.objects.get(id=id)

    if request.method == 'POST':
        form = SaidaForm(request.POST, instance=saida_obj)

        if form.is_valid():

            if not saida_obj.saida_item.exists():
                form.save()
                return redirect('saida_edit', saida_id=saida_obj.id)
            else:
                return HttpResponseNotFound('<h1>Saida com itens, para alterar exclua os itens primeiro</h1>')
    else:
        form = SaidaForm()
    context = {
        'form': form,
    }
    return render(request, 'interface/saida/saida_edit.html', context)


@login_required
def saida_delete(request, id):
    saida_obj = Saida.objects.get(id=id)

    if saida_obj.saida_item.exists():
        return HttpResponseNotFound('<h1>Saída com itens</h1>')
    else:
        saida_obj.delete()
        return redirect(saida)


# Itens Saída

@login_required
def itemSaida_create(request, saida_id):
    saida_obj = Saida.objects.get(id=saida_id)

    if request.method == 'POST':
        item_form = Item_SaidaForm(request.POST)

        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.saida = saida_obj

            if item.produto_saida.estoque >= item.amount_produto and saida_obj.date_create >= item.produto_saida.data:
                item.save()

                produto_obj = Produto.objects.get(id=item.produto_saida.id)
                produto_obj.estoque -= item.amount_produto
                produto_obj.save()
                return redirect('saida_edit', saida_id=saida_id)
            else:
                return HttpResponseNotFound('<h1>Item sem saldo</h1>')

    else:
        item_form = Item_SaidaForm()

    context = {
        'item_form': item_form,
    }
    return render(request, 'interface/saida/saida_edit.html', context)


@login_required
def itemSaida_delete(request, id):
    item_saida = Item_Saida.objects.get(id=id)
    item_saida.delete()

    produto_obj = Produto.objects.get(id=item_saida.produto_saida.id)
    produto_obj.estoque += item_saida.amount_produto
    produto_obj.save()
    return redirect(request.META.get('HTTP_REFERER'))


# Estoque

@login_required
def estoque(request):
    return render(request, 'interface/estoque/estoque.html')


@login_required
def estoque_day(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        try:
            datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            context = {'error_message': 'A data deve estar no formato YYYY-MM-DD.'}
            return render(request, 'interface/estoque/estoque.html', context)

        produtos = Produto.objects.filter(data=data)
        context = {
            'data': data,
            'produtos': produtos,
        }
        return render(request, 'interface/estoque/estoque.html', context)
    else:
        produtos = []
        context = {
            'produtos': produtos,
        }
        return render(request, 'interface/estoque/estoque.html', context)

