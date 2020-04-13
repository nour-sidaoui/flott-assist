from django.contrib import admin
from django.urls import include, path

from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', include('dashboard.urls')),
    path('conducteur/', include('conducteur.urls')),
    path('vehicules/', include('vehicule.urls')),
    path('conducteurs/', include('employe.urls')),
    path('historique/', include('historique.urls')),
    path('accounts/', include('django.contrib.auth.urls'), name='logout'),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

