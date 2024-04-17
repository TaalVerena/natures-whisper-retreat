"""
URL configuration for natures_whisper project.

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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("lodges/", include("lodges.urls"), name="lodges-urls"),
    path("reservations/", include("reservations.urls")),
    path("", include("home.urls"), name="home-urls"),
    path("", include("contact.urls"), name="contact-urls"),
    path("", include("about.urls"), name="about-urls"),
    path("", include("dashboard.urls"), name="dashboard-urls"),
    path("summernote/", include("django_summernote.urls")),
    path("api/", include("reservations.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
