from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("escola/", include("escola.urls")),
    path("portfolio/", include("portfolio.urls")),
    path("accounts/", include("accounts.urls")),
    path("artigos/", include("artigos.urls")),
    path("", lambda request: redirect('/portfolio/')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)