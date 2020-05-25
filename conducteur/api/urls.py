from django.urls import path
from rest_framework.authtoken import views
from conducteur.api.views import (api_km_prise,
                                  api_km_restit,
                                  api_voir_prob,
                                  api_declarer_prob,
                                  api_modifer_prob,
                                  api_gps,
                                  api_get_veh
                                  )


app_name = 'api_conducteur'

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('km_in/', api_km_prise, name='km_in'),
    path('km_in', api_km_prise, name='km_in'),
    path('km_out/', api_km_restit, name='km_out'),
    path('voir_probleme/', api_voir_prob, name='voir_probleme'),
    path('declarer_probleme/', api_declarer_prob, name='declarer_probleme'),
    path('modifier_probleme/', api_modifer_prob, name='modifer_probleme'),
    path('gps/', api_gps, name='partage_gps'),
    path('get_veh/', api_get_veh, name='get_immat'),
]

