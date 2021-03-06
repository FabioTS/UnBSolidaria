from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Urls para usuarios nao logados
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^noticias/$', views.noticias, name="noticias"),
    url(r'^contato/$', views.contato, name="contato"),
    url(r'^faq/$', views.faq, name="faq"),
    url(r'^listaTrabalhos/$', views.TrabalhosView.as_view(), name="lista-trabalhos"),
    url(r'^criarTrabalho/$', views.TrabalhoCreate.as_view(), name="criar-trabalho"),
    url(r'^editarTrabalho/(?P<pk>\d+)/$', views.TrabalhoUpdate.as_view(), name="editar-trabalho"),
    url(r'^deletarTrabalho/(?P<pk>\d+)/$', views.TrabalhoDelete.as_view(), name="deletar-trabalho"),
    url(r'^visualizarTrabalho/(?P<pk>\d+)/$', views.TrabalhoDetailView.as_view(), name='visualizar-trabalho'),
    url(r'^registrar/$', views.UserFormView.as_view(), name='registrar'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    # url(r'^login/$', views.login, name="login"),
    # url(r'^signup/$', views.signup, name="signup"),
]
