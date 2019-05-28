from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'api/login.html'}, name='loginGrafica'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/grafica/login/'}, name='logoutGrafica'),
    url(r'^main/$', views.index, name='main'),
    url(r'^arquivo/$', views.arquivo, name='arquivo'),
    url(r'negar/(?P<negar_id>[0-9]+)$', views.negar, name='negar'),
    url(r'impresso/(?P<imp_id>[0-9]+)/(?P<matricula>[0-9]+)$', views.impresso, name='impresso'),
    url(r'^autenticar/(?P<matricula>[0-9]+)$', views.autenticar, name='autenticar'),
    url(r'^status/(?P<matricula>[0-9]+)$', views.status, name='status'),
    url(r'^addsaldo/$', views.saldo, name='addsaldo'),
    url(r'^impressoes/$', views.todas_impressoes, name='todas'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
