from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'employe'

urlpatterns = [
    path('', views.index, name='index'),
    path('conducteurs/', views.page_conducteurs, name='page_conducteurs'),
    path('conducteurs/ajouter/', views.ajouter, name='ajouter_cond'),
    path('conducteurs/modifier/', views.ajouter, name='modifier'),
    path('conducteurs/voir_profil/<int:pk>/', views.voir_profil, name='voir_profil')
]

# url('conducteurs/voir_profil/(?P<pk>\w+)/$', views.voir_profil, name='voir_profil')