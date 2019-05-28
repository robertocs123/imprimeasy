from django import forms
from django.forms import ModelForm
from api.models import Usuario, Arquivo


class Login(forms.Form):
	matricula = forms.CharField(label='Matricula', max_length=14)
	senha = forms.CharField(label='Senha', max_length=20)


class Impressao(ModelForm):
	class Meta:
		model= Arquivo
		fields = ['arquivo','copias','cor','obs']


class Impressao2(forms.Form):
	arquivo = forms.FileField(label= 'Arquivo')
	copias = forms.CharField(label='Copias')
	cor = forms.CharField(label='Cor')
	obs = forms.CharField(label= 'Obs',max_length = 1000)

