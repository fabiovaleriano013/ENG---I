from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404, render, redirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.serializers import serialize


def is_industria_member(user):
    return user.groups.filter(name='Industria').exists() or user.is_superuser

@login_required
@user_passes_test(is_industria_member)
def index(request):
    # Printe os campos do modelo Ingrediente para entender como acessar os dados
    print(Ingredientes._meta.fields)
    return render(request, 'index_industria.html')
    

@login_required
@user_passes_test(is_industria_member)
def ordem_producao(request):
    ordem_producoes = OrdemProducao.objects.all()
    context = {'ordem_producoes': ordem_producoes}

    return render(request, 'ordem_producao.html', context)

@login_required
@user_passes_test(is_industria_member)
def produto(request):
    produtos = Produto.objects.all()
    context = {'produtos': produtos}

    return render(request, 'produto.html', context)

@login_required
@user_passes_test(is_industria_member)
def custo(request):
    custos = CustoGeral.objects.all()
    context = {'custos': custos}

    return render(request, 'custos.html', context)
    

@login_required
@user_passes_test(is_industria_member)
def materia_prima(request):
    materias_primas = MateriaPrima.objects.all()
    context = {'materias_primas': materias_primas}

    return render(request, 'materia_prima.html', context)

@login_required
@user_passes_test(is_industria_member)
def entrada_produto(request):
    entrada_produtos = EntradaProduto.objects.all()
    context = {'entrada_produtos': entrada_produtos}

    return render(request, 'entrada_produto.html', context)

@login_required
@user_passes_test(is_industria_member)
def saida_produto(request):
    saida_produtos = SaidaProduto.objects.all()
    context = {'saida_produtos': saida_produtos}

    return render(request, 'saida_produto.html', context)

@login_required
@user_passes_test(is_industria_member)
def create_entrada_produto(request):
    if request.method == 'GET':
        entrada_produto_form = EntradaProdutoForm()
        entrada_produto_item_form_factory = inlineformset_factory(EntradaProduto, EntradaProdutoItem, form=EntradaProdutoItemForm, extra=1)
        entrada_produto_item_form = entrada_produto_item_form_factory()
        context = {'entrada_produto_form': entrada_produto_form, 'entrada_produto_item_form': entrada_produto_item_form}

        return render(request, 'create_update_entrada_produto.html', context)
    elif request.method == 'POST':
        entrada_produto_form = EntradaProdutoForm(request.POST)
        entrada_produto_item_form_factory = inlineformset_factory(EntradaProduto, EntradaProdutoItem, form=EntradaProdutoItemForm)
        entrada_produto_item_form = entrada_produto_item_form_factory(request.POST)

        if entrada_produto_form.is_valid() and entrada_produto_item_form.is_valid():
            entrada_produto = entrada_produto_form.save(commit=False)
            entrada_produto_item_form.instance = entrada_produto       
            entrada_produto_form.save()
            entrada_produto_item_form.save()

            messages.success(request, 'Produto cadastrado com sucesso!')

            return redirect('entrada_produto')
        else:
            messages.error(request, 'Erro ao cadastrar o produto!')

            context = {'entrada_produto_form': entrada_produto_form, 'entrada_produto_item_form': entrada_produto_item_form}

            return render(request, 'create_update_entrada_produto.html', context)

@login_required
@user_passes_test(is_industria_member)
def read_entrada_produto(request, id):
    entrada_produto = EntradaProduto.objects.get(id=id)
    context = {'entrada_produto': entrada_produto}

    return render(request, 'read_entrada_produto.html', context)

@login_required
@user_passes_test(is_industria_member)
def update_entrada_produto(request, id):
    entrada_produto = get_object_or_404(EntradaProduto, id=id)

    if request.method == 'GET':
        if entrada_produto is None:
            messages.error(request, 'Registro não encontrado!')

            return redirect('entrada_produto')
        
        entrada_produto_form = EntradaProdutoForm(instance=entrada_produto)
        entrada_produto_item_form_factory = inlineformset_factory(EntradaProduto, EntradaProdutoItem, form=EntradaProdutoItemForm, extra=0)
        entrada_produto_item_form = entrada_produto_item_form_factory(instance=entrada_produto)
        context = {'entrada_produto_form': entrada_produto_form, 'entrada_produto_item_form': entrada_produto_item_form}

        return render(request, 'create_update_entrada_produto.html', context)
    elif request.method == 'POST':
        if entrada_produto is None:
            messages.error(request, 'Registro não encontrado!')

            return redirect('entrada_produto')
        
        entrada_produto_form = EntradaProdutoForm(request.POST, instance=entrada_produto)
        entrada_produto_item_form_factory = inlineformset_factory(EntradaProduto, EntradaProdutoItem, form=EntradaProdutoItemForm)
        entrada_produto_item_form = entrada_produto_item_form_factory(request.POST, instance=entrada_produto)

        if entrada_produto_item_form.is_valid() and entrada_produto_item_form.is_valid():
            entrada_produto = entrada_produto_form.save(commit=False)
            entrada_produto_item_form.instance = entrada_produto
            entrada_produto.save()
            entrada_produto_item_form.save()

            messages.success(request, 'Produto atualizado com sucesso!')

            return redirect('entrada_produto')
        else:
            context = {'entrada_produto_form': entrada_produto_form, 'entrada_produto_item_form': entrada_produto_item_form}

            messages.error(request, 'Erro ao atualizar produto!')

            return render(request, 'create_update_entrada_produto.html', context)

@login_required
@user_passes_test(is_industria_member)
def delete_entrada_produto(request, id):
    entrada_produto = get_object_or_404(EntradaProduto, id=id)

    if request.method == 'POST':
        entrada_produto.delete()
        
        return JsonResponse({'message': 'Produto excluído com sucesso!'})

    return JsonResponse({'message': 'Método não permitido'}, status=405)



@login_required
@user_passes_test(is_industria_member)
def create_materia_prima(request):
    if request.method == 'GET':
        materia_prima_form = MateriaPrimaForm()
        context = {'materia_prima_form': materia_prima_form}

        return render(request, 'create_update_materia_prima.html', context)
    elif request.method == 'POST':
        materia_prima_form = MateriaPrimaForm(request.POST)

        if materia_prima_form.is_valid():
            materia_prima_form.save()

            messages.success(request, 'Matéria-prima cadastrada com sucesso!')

            return redirect('materia_prima')
        else:
            messages.error(request, 'Erro ao cadastrar a matéria-prima!')

            context = {'materia_prima_form': materia_prima_form}

            return render(request, 'create_update_materia_prima.html', context)
        
@login_required
@user_passes_test(is_industria_member)
def read_materia_prima(request, id):
    materia_prima = MateriaPrima.objects.get(id=id)
    context = {'materia_prima': materia_prima}

    return render(request, 'read_materia_prima.html', context)


@login_required
@user_passes_test(is_industria_member)
def update_materia_prima(request, id):
    materia_prima = get_object_or_404(MateriaPrima, id=id)

    if request.method == 'GET':
        if materia_prima is None:
            messages.error(request, 'Registro não encontrado!')

            return redirect('materia_prima')

        materia_prima_form = MateriaPrimaForm(instance=materia_prima)
        context = {'materia_prima_form': materia_prima_form}

        return render(request, 'create_update_materia_prima.html', context)
    elif request.method == 'POST':
        if materia_prima is None:
            messages.error(request, 'Registro não encontrado!')

            return redirect('materia_prima')

        materia_prima_form = MateriaPrimaForm(request.POST, instance=materia_prima)

        if materia_prima_form.is_valid():
            materia_prima_form.save()

            messages.success(request, 'Matéria-prima atualizada com sucesso!')

            return redirect('materia_prima')
        else:
            context = {'materia_prima_form': materia_prima_form}

            messages.error(request, 'Erro ao atualizar matéria-prima!')

            return render(request, 'create_update_materia_prima.html', context)
        

@login_required
@user_passes_test(is_industria_member)
def delete_materia_prima(request, id):
    materia_prima = get_object_or_404(MateriaPrima, id=id)

    if request.method == 'POST':
        materia_prima.delete()

        return JsonResponse({'message': 'Matéria-prima excluída com sucesso!'})

    return JsonResponse({'message': 'Método não permitido'}, status=405)


@login_required
@user_passes_test(is_industria_member)
def create_produto(request):
    if request.method == 'GET':
        produto_form = ProdutoForm()
        context = {'produto_form': produto_form}

        return render(request, 'create_update_produto.html', context)
    elif request.method == 'POST':
        produto_form = ProdutoForm(request.POST)

        if produto_form.is_valid():
            produto_form.save()

            messages.success(request, 'Produto cadastrado com sucesso!')

            return redirect('produto')
        else:
            messages.error(request, 'Erro ao cadastrar o produto!')

            context = {'produto_form': produto_form}

            return render(request, 'create_update_produto.html', context)
        
@login_required
@user_passes_test(is_industria_member)
def read_produto(request, id):
    produto = Produto.objects.get(id=id)
    context = {'produto': produto}

    return render(request, 'read_produto.html', context)

@login_required
@user_passes_test(is_industria_member)
def update_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'GET':
        if produto is None:
            messages.error(request, 'Registro não encontrado!')

            return redirect('produto')

        produto_form = ProdutoForm(instance=produto)
        context = {'produto_form': produto_form}

        return render(request, 'create_update_produto.html', context)
    elif request.method == 'POST':
        if produto is None:
            messages.error(request, 'Registro não encontrado!')

            return redirect('produto')

        produto_form = ProdutoForm(request.POST, instance=produto)

        if produto_form.is_valid():
            produto_form.save()

            messages.success(request, 'Produto atualizado com sucesso!')

            return redirect('produto')
        else:
            context = {'produto_form': produto_form}

            messages.error(request, 'Erro ao atualizar produto!')

            return render(request, 'create_update_produto.html', context)
        
@login_required
@user_passes_test(is_industria_member)
def delete_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        produto.delete()

        return JsonResponse({'message': 'Produto excluído com sucesso!'})

    return JsonResponse({'message': 'Método não permitido'}, status=405)

@login_required
@user_passes_test(is_industria_member)
def create_saida_produto(request):
    if request.method == 'GET':
        saida_produto_form = SaidaProdutoForm()
        saida_produto_item_form_factory = inlineformset_factory(SaidaProduto, SaidaProdutoItem, form=SaidaProdutoItemForm, extra=1)
        saida_produto_item_form = saida_produto_item_form_factory()
        context = {'saida_produto_form': saida_produto_form, 'saida_produto_item_form': saida_produto_item_form}

        return render(request, 'create_update_saida_produto.html', context)
    elif request.method == 'POST':
        saida_produto_form = SaidaProdutoForm(request.POST)
        saida_produto_item_form_factory = inlineformset_factory(SaidaProduto, SaidaProdutoItem, form=SaidaProdutoItemForm)
        saida_produto_item_form = saida_produto_item_form_factory(request.POST)

        if saida_produto_form.is_valid() and saida_produto_item_form.is_valid():
            saida_produto = saida_produto_form.save(commit=False)
            saida_produto_item_form.instance = saida_produto
            saida_produto_form.save()
            saida_produto_item_form.save()

            messages.success(request, 'Produto cadastrado com sucesso!')

            return redirect('saida_produto')
        else:
            messages.error(request, 'Erro ao cadastrar o produto!')

            context = {'saida_produto_form': saida_produto_form, 'saida_produto_item_form': saida_produto_item_form}

            return render(request, 'create_update_saida_produto.html', context)

@login_required
@user_passes_test(is_industria_member)
def read_saida_produto(request, id):
    saida_produto = SaidaProduto.objects.get(id=id)
    context = {'saida_produto': saida_produto}

    return render(request, 'read_saida_produto.html', context)


@login_required
@user_passes_test(is_industria_member)
def update_saida_produto(request, id):
    saida_produto = get_object_or_404(SaidaProduto, id=id)

    if request.method == 'GET':
        if saida_produto is None:
            messages.error(request, 'Registro não encontrado!')

            return redirect('saida_produto')

        saida_produto_form = SaidaProdutoForm(instance=saida_produto)
        saida_produto_item_form_factory = inlineformset_factory(SaidaProduto, SaidaProdutoItem, form=SaidaProdutoItemForm, extra=0)
        saida_produto_item_form = saida_produto_item_form_factory(instance=saida_produto)
        context = {'saida_produto_form': saida_produto_form, 'saida_produto_item_form': saida_produto_item_form}

        return render(request, 'create_update_saida_produto.html', context)
    elif request.method == 'POST':
        if saida_produto is None:
            messages.error(request, 'Registro não encontrado!')

            return redirect('saida_produto')

        saida_produto_form = SaidaProdutoForm(request.POST, instance=saida_produto)
        saida_produto_item_form_factory = inlineformset_factory(SaidaProduto, SaidaProdutoItem, form=SaidaProdutoItemForm)
        saida_produto_item_form = saida_produto_item_form_factory(request.POST, instance=saida_produto)

        if saida_produto_item_form.is_valid() and saida_produto_item_form.is_valid():
            saida_produto = saida_produto_form.save(commit=False)
            saida_produto_item_form.instance = saida_produto
            saida_produto.save()
            saida_produto_item_form.save()

            messages.success(request, 'Produto atualizado com sucesso!')

            return redirect('saida_produto')
        else:
            context = {'saida_produto_form': saida_produto_form, 'saida_produto_item_form': saida_produto_item_form}

            messages.error(request, 'Erro ao atualizar produto!')

            return render(request, 'create_update_saida_produto.html', context)

@login_required
@user_passes_test(is_industria_member)
def delete_saida_produto(request, id):
    saida_produto = get_object_or_404(SaidaProduto, id=id)

    if request.method == 'POST':
        saida_produto.delete()

        return JsonResponse({'message': 'Produto excluído com sucesso!'})

    return JsonResponse({'message': 'Método não permitido'}, status=405)

@login_required
@user_passes_test(is_industria_member)
def create_ordem_producao(request):
    if request.method == 'GET':
        ordem_producao_form = OrdemProducaoForm()
        ordem_producao_produto_form_factory = inlineformset_factory(OrdemProducao, OrdemProducaoProduto, form=OrdemProducaoProdutoForm, extra=1)
        ordem_producao_produto_form = ordem_producao_produto_form_factory()
        context = {'ordem_producao_form': ordem_producao_form, 'ordem_producao_produto_form': ordem_producao_produto_form}

        return render(request, 'create_update_ordem_producao.html', context)
    elif request.method == 'POST':
        ordem_producao_form = OrdemProducaoForm(request.POST)
        ordem_producao_produto_form_factory = inlineformset_factory(OrdemProducao, OrdemProducaoProduto, form=OrdemProducaoProdutoForm)
        ordem_producao_produto_form = ordem_producao_produto_form_factory(request.POST)

        if ordem_producao_form.is_valid() and ordem_producao_produto_form.is_valid():
            ordem_producao = ordem_producao_form.save(commit=False)
            ordem_producao_produto_form.instance = ordem_producao
            ordem_producao_form.save()
            ordem_producao_produto_form.save()

            messages.success(request, 'Ordem de produção iniciada com sucesso!')

            return redirect('ordem_producao')
        else:
            messages.error(request, 'Erro ao iniciar ordem de produção!')

            context = {'ordem_producao_form': ordem_producao_form, 'ordem_producao_produto_form': ordem_producao_produto_form}

            return render(request, 'create_update_ordem_producao.html', context)

@login_required
@user_passes_test(is_industria_member)
def read_ordem_producao(request, id):
    ordem_producao = OrdemProducao.objects.get(id=id)
    context = {'ordem_producao': ordem_producao}

    return render(request, 'read_ordem_producao.html', context)

@login_required
@user_passes_test(is_industria_member)
def update_ordem_producao(request, id):
    ordem_producao = get_object_or_404(OrdemProducao, id=id)

    if request.method == 'GET':
        if ordem_producao is None:
            messages.error(request, 'Ordem não encontrada!')

            return redirect('ordem_producao')

        ordem_producao_form = OrdemProducaoForm(instance=ordem_producao)
        ordem_producao_produto_form_factory = inlineformset_factory(OrdemProducao, OrdemProducaoProduto, form=OrdemProducaoProdutoForm, extra=0)
        ordem_producao_produto_form = ordem_producao_produto_form_factory(instance=ordem_producao)
        context = {'ordem_producao_form': ordem_producao_form, 'ordem_producao_produto_form': ordem_producao_produto_form}

        return render(request, 'create_update_ordem_producao.html', context)
    elif request.method == 'POST':
        if ordem_producao is None:
            messages.error(request, 'Ordem não encontrada!')

            return redirect('ordem_producao')

        ordem_producao_form = OrdemProducaoForm(request.POST, instance=ordem_producao)
        ordem_producao_produto_form_factory = inlineformset_factory(OrdemProducao, OrdemProducaoProduto, form=OrdemProducaoProdutoForm)
        ordem_producao_produto_form = ordem_producao_produto_form_factory(request.POST, instance=ordem_producao)

        if ordem_producao_produto_form.is_valid() and ordem_producao_produto_form.is_valid():
            ordem_producao = ordem_producao_form.save(commit=False)
            ordem_producao_produto_form.instance = ordem_producao
            ordem_producao.save()
            ordem_producao_produto_form.save()

            messages.success(request, 'Ordem atualizado com sucesso!')

            return redirect('ordem_producao')
        else:
            context = {'ordem_producao_form': ordem_producao_form, 'ordem_producao_produto_form': ordem_producao_produto_form}

            messages.error(request, 'Erro ao atualizar ordem!')

            return render(request, 'create_update_ordem_producao.html', context)

@login_required
@user_passes_test(is_industria_member)
def delete_ordem_producao(request, id):
    ordem_producao = get_object_or_404(OrdemProducao, id=id)

    if request.method == 'POST':
        ordem_producao.delete()

        return JsonResponse({'message': 'Ordem cancelada com sucesso!'})

    return JsonResponse({'message': 'Método não permitido'}, status=405)


def custo_receita(request, id):
    receita = get_object_or_404(Receita, id=id)
    data = [receita]
    data_serializada = serialize('json', data, use_natural_foreign_keys=True)
    return JsonResponse(data_serializada, safe=False)

def ingrediente(request, id):
    receita = get_object_or_404(Receita, id=id)
    ingredientes = Ingredientes.objects.filter(receita_id=receita).select_related('materia_prima')
    print(ingredientes)
    data_serializada = serialize('json', ingredientes, use_natural_foreign_keys=True)
    return JsonResponse(data_serializada, safe=False)

def embalagem(request, id):
    receita = get_object_or_404(Receita, id=id)
    embalagens = Embalagens.objects.filter(receita_id=receita).select_related('nome_tipo_embalagem')
    print(embalagens)
    data_serializada = serialize('json', embalagens, use_natural_foreign_keys=True)
    return JsonResponse(data_serializada, safe=False)

def producao_funcionario(request, id):
    receita = get_object_or_404(Receita, id=id)
    producao_funcionario = ProducaoFuncionario.objects.filter(receita_id=receita).select_related('funcionario')
    print(producao_funcionario)
    data_serializada = serialize('json', producao_funcionario, use_natural_foreign_keys=True)
    return JsonResponse(data_serializada, safe=False)


