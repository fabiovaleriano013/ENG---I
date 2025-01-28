from django import forms
from .models import *

class contatoForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'