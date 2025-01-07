from django import forms
from .models import *

class EntradaProdutoForm(forms.ModelForm):
    class Meta:
        model = EntradaProduto
        fields = '__all__'

    data_hora = forms.DateTimeField(
        widget=forms.TextInput(attrs={"type": "datetime-local"}),
        input_formats=["%Y-%m-%dT%H:%M"],
    )
        
class EntradaProdutoItemForm(forms.ModelForm):
    class Meta:
        model = EntradaProdutoItem
        fields = '__all__'


class SaidaProdutoForm(forms.ModelForm):
    class Meta:
        model = SaidaProduto
        fields = '__all__'

    data_hora = forms.DateTimeField(
        widget=forms.TextInput(attrs={"type": "datetime-local"}),
        input_formats=["%Y-%m-%dT%H:%M"],
    )
        
class SaidaProdutoItemForm(forms.ModelForm):
    class Meta:
        model = SaidaProdutoItem
        fields = '__all__'

class OrdemProducaoForm(forms.ModelForm):
    class Meta:
        model = OrdemProducao
        fields = '__all__'

    data_producao = forms.DateTimeField(
        widget=forms.TextInput(attrs={"type": "datetime-local"}),
        input_formats=["%Y-%m-%dT%H:%M"],
        required=False

    )
        
class OrdemProducaoProdutoForm(forms.ModelForm):
    class Meta:
        model = OrdemProducaoProduto
        fields = '__all__'

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'

class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        #todos os fields menos tipo
        fields = ['nome_materia_prima', 'grupo', 'unidade_medida', 'marca', 'fabricante']

class CustoGeralForm(forms.ModelForm):
    class Meta:
        model = CustoGeral
        fields = '__all__'

class CustoGeralItemForm(forms.ModelForm):
    class Meta:
        model = SubCentroDeCusto
        fields = '__all__'