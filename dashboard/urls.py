from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('attribuer/', views.attribuer_veh, name='attribuer_vehicule'),
    path('restituer/', views.restituer_veh, name='restituer_vehicule'),
    path('ajax/charger-vehicules/', views.charger_vehicules, name='ajax_charger_vehicules'),
]
