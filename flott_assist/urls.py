"""flott_assist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')

Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('dashboard.urls')),
    path('vehicules/', include('vehicule.urls')),
    path('conducteurs/', include('employe.urls')),
    path('historique/', include('historique.urls')),
    path('accounts/', include('django.contrib.auth.urls'), name='logout'),
    path('admin/', admin.site.urls),
]


