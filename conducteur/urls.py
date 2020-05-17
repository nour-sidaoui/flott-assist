from django.urls import path
from . import views

app_name = 'conducteur'

urlpatterns = [
    path('', views.index, name='index'),
    path('enregistrer_km_entree/', views.page_km_in, name='km_in'),
    path('enregistrer_km_sortie/', views.page_km_out, name='km_out'),
    path('declarer_probleme/', views.declarer_prob, name='declarer_prob'),
    path('contacter_assistance/', views.contacter_assist, name='contact_assist'),
    ]
