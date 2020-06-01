"""adminka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from authentication import urls as authentication_urls
from management import urls as management_urls
from django.conf.urls.static import static
from django.urls import path, include
from common import urls as cmmon_urls
from django.contrib import admin
from adminka import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('management/', include(management_urls, namespace='management')),
    path('', include(cmmon_urls, namespace='common')),
    path('auth/', include(authentication_urls, namespace='authentication')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
