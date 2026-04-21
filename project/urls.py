## ficheiro projects/urls.py

from django.contrib import admin
from django.urls import path, include              #     <- adicionar include 
from django.conf import settings
from django.conf.urls.static import static

## project/urls.py

urlpatterns = [
    path("admin/", admin.site.urls),
    path("escola/", include("escola.urls")), 
    path("", include("escola.urls")),  #  rota para app escola sem precisar de escrever "escola"
]

# Serve ficheiros media em DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)