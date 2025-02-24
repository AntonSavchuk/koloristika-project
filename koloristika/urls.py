"""
URL configuration for koloristika project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static

from . import settings
from users.views import profile_view

urlpatterns = [
    path("", include("main.urls", namespace='main')),
    path("services/", include("services.urls", namespace='services')),
    path('newsletter/', include('newsletter.urls', namespace='newsletter')),
    path('accounts/', include('allauth.urls')),
    path("profile/", profile_view, name="account_profile"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)