from django.urls import path
from . import views

app_name = 'historique'


urlpatterns = [
    path('', views.page_recherche, name='page_recherche'),
]
