from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('messages/', views.msg, name='msg'),
    path('voir_message/<int:pk>/', views.voir_msg, name='voir_msg'),
    path('attribuer/', views.attribuer_veh, name='attribuer_vehicule'),
    path('restituer/', views.restituer_veh, name='restituer_vehicule'),
    path('ajouter-amende/', views.ajouter_amende, name='ajouter_amende'),
    path('saisir-entretien/', views.saisir_entretien, name='saisir_entretien'),
    path('ajax/charger-vehicules/', views.charger_vehicules, name='ajax_charger_vehicules'),
]
