from django.contrib import admin

from .models import Usuario, Arquivo
# Register your models here.

class ArquivoAdmin(admin.ModelAdmin):
	model = Arquivo
	list_display = ['nome', 'usuario', 'status']
	list_filter = ['status']
	search_fields = ['nome']
	save_on_top = False

admin.site.register(Usuario)
admin.site.register(Arquivo, ArquivoAdmin)