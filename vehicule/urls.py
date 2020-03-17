from django.urls import path
from . import views

app_name = 'vehicule'


urlpatterns = [
    path('', views.page_vehicules, name='page_vehicules'),
    path('ajouter/', views.ajouter_veh, name='ajouter_vehicule'),
    path('fiche_vehicule/<int:pk>/', views.fiche_vehicule, name='fiche_veh')
]
