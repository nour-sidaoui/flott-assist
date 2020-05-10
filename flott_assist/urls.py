from django.contrib import admin
from django.urls import include, path

from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

    # MAIN APPS
    path('', include('dashboard.urls')),
    path('conducteur/', include('conducteur.urls')),
    path('vehicules/', include('vehicule.urls')),
    path('conducteurs/', include('employe.urls')),
    path('historique/', include('historique.urls')),

    # DJANGO URLS (ADMIN)
    path('accounts/', include('django.contrib.auth.urls'), name='logout'),

    # ADMIN URLS
    path('admin/', admin.site.urls),

    # REST FRAMEWORK URLS
    path('api/', include('conducteur.api.urls')),

    # UPDATE URL
    path('update_server/', include('updater.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

