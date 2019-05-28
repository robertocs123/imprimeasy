from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    url(r'^login/$', auth_views.login, {'template_name': 'aluno/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}, name='logout'),
    url(r'^checando_login/$', views.login, name='checar'),
    url(r'^menu/$', views.index, name='menu'),   
    url(r'^autenticar/(?P<matricula>[0-9]+)$', views.autenticar, name='autenticar'),
    url(r'^verificando_saldo/$', views.saldo, name='saldo'),
    url(r'^solicitar/$', views.solicitar, name='solicitar'),
    url(r'^historico/$', views.historico, name='historico'),  
    url(r'^enviando/$', views.enviarImprimir, name='enviar'),
 
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
