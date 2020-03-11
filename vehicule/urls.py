from django.urls import path
from . import views

app_name = 'vehicule'


urlpatterns = [
    path('', views.page_vehicules, name='page_vehicules'),
    path('ajouter/', views.ajouter, name='ajouter'),
    path('fiche_vehicule/<int:veh_id>/', views.fiche_vehicule, name='fiche_veh')
]
