from django.db import models

class Usuario(models.Model):
	matricula = models.CharField(max_length=30)
	saldo = models.FloatField(default=0.0)
	registro = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.matricula
# acrescentar transações para o usuario saber o que aconteceu com seu dinheiro
class Transacao(models.Model):
	usuario = models.ForeignKey(Usuario)
	valor = models.FloatField(default = 0.00)
	data = models.DateTimeField(auto_now_add=True)
#

class Arquivo(models.Model):
	IMPRESSO = 1
	AGUARDANDO = 2
	NEGADO = 3
	STATUS_CHOICES = (
	    (IMPRESSO, 'Impresso'),
	    (AGUARDANDO, 'Aguardando aprovação'),
	    (NEGADO, 'Impressão negada'),
	)
	#
	COLORIDO = 1
	PRETO_E_BRANCO = 0
	COR_CHOICES = (
		(COLORIDO, 'Colorido'),
		(PRETO_E_BRANCO, 'Preto e branco'), #Preto e branco aparece para o usuario, PRETO_E_BRANCO APARECE é salvo no banco

	 )
    #


	nome = models.CharField(max_length=100)
	usuario = models.ForeignKey(Usuario)
   #
	data = models.DateTimeField(auto_now_add=True) #default = timezone.now
	copias = models.IntegerField(default= 1)
	cor = models.IntegerField( choices=COR_CHOICES, default = PRETO_E_BRANCO )
	obs = models.CharField(max_length = 1000, default = 'Sem obs.')
	valor = models.FloatField(default = 0.00)
	arquivo = models.FileField(default='Arquivo não encontrado')
   #
	url = models.CharField(max_length=150)
	status = models.IntegerField(choices=STATUS_CHOICES, default=AGUARDANDO)

	def __str__(self):
		return self.nome
