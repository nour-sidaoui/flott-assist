from django.urls import path

'''
here the name of my app is updater so I add the import my view from there
replace updater with your app-name where you have your views.py
'''
from updater import views

app_name = 'updater'

urlpatterns = [
    path("", views.update, name="update"),
]
