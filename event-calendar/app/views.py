from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404, render, redirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.serializers import serialize


def index(request):
    # Printe os campos do modelo Ingrediente para entender como acessar os dados
    return render(request, 'index.html')
    
def contato(request):
    contatos = Contact.objects.all()
    context = {'contatos': contatos}
    return render(request, 'contato.html', context)



def create_contato(request):
    if request.method == 'GET':
        contato_form = contatoForm()
        context = {'contato_form': contato_form}

        return render(request, 'create_update_contato.html', context)
    elif request.method == 'POST':
        contato_form = contatoForm(request.POST)

        if contato_form.is_valid():
            contato_form.save()

            messages.success(request, 'contato cadastrado com sucesso!')

            return redirect('contato')
        else:
            messages.error(request, 'Erro ao cadastrar o contato!')

            context = {'contato_form': contato_form}

            return render(request, 'create_update_contato.html', context)
        





def update_contato(request, id):
    contato = get_object_or_404(Contact, id=id)

    if request.method == 'GET':
        if contato is None:
            messages.error(request, 'Registro não encontrado!')

            return redirect('contato')

        contato_form = contatoForm(instance=contato)
        context = {'contato_form': contato_form}

        return render(request, 'create_update_contato.html', context)
    elif request.method == 'POST':
        if contato is None:
            messages.error(request, 'Registro não encontrado!')

            return redirect('contato')

        contato_form = contatoForm(request.POST, instance=contato)

        if contato_form.is_valid():
            contato_form.save()

            messages.success(request, 'contato atualizado com sucesso!')

            return redirect('contato')
        else:
            context = {'contato_form': contato_form}

            messages.error(request, 'Erro ao atualizar contato!')

            return render(request, 'create_update_contato.html', context)
        


def delete_contato(request, id):
    contato = get_object_or_404(Contact, id=id)

    if request.method == 'POST':
        contato.delete()

        return JsonResponse({'message': 'contato excluído com sucesso!'})

    return JsonResponse({'message': 'Método não permitido'}, status=405)





