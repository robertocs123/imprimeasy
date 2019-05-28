from django import forms
from django.forms import ModelForm
from .models import Usuario, Arquivo

class Aluno(ModelForm):
	class Meta:
		model= Arquivo
		fields = ['nome','copias','cor','obs']

class Saldo(forms.Form):
	matricula = forms.CharField(label='Matricula', max_length=14)
	valor = forms.CharField(label='Valor', max_length=20)