from django.urls import path
from . import views

app_name = 'employe'

urlpatterns = [
    path('', views.page_conducteurs, name='page_conducteurs'),
    path('ajouter/', views.ajouter, name='ajouter_cond'),
    path('modifier/', views.ajouter, name='modifier'),
    path('voir_profil/<int:pk>/', views.voir_profil, name='voir_profil')
]
