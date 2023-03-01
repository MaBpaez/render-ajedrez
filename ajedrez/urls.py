"""ajedrez URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
# from normativa import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path CKEDITOR
    path("ckeditor/", include("ckeditor_uploader.urls")),
    # Path CORE
    path("", include('core.urls', namespace='torneo')),
    # Path CONTACTO
    path("contacto/", include('contacto.urls', namespace='contacto')),
    # Path NORMATIVA
    path("normativas/", include('normativa.urls', namespace='normativa')),
    # Path BLOG
    path('blog/', include('blog.urls', namespace='blog')),
    # Path CIRCUITO DIPUTACION
    path('circuito-diputacion/', include('circuitos.urls', namespace="circuitos")),
    # Path ESCUELAS Y CLUBES
    path('clubes-de-ajedrez/', include('escuelas.urls', namespace="escuelas")),
    # Path PAGE
    path("pagina/", include("page.urls", namespace="pagina")),
]

admin.site.site_header = 'Administración AjedrezMálaga'

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
