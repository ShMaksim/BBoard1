"""
URL configuration for board project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from ads.views import post_list, post_detail, post_create, post_edit, response_list, change_response_status, subscribe, send_newsletter, confirm_email
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', post_list, name='post_list'),
    path('ads/<int:pk>/', post_detail, name='post_detail'),
    path('ads/create/', post_create, name='post_create'),
    path('ads/<int:pk>/edit/', post_edit, name='post_edit'),
    path('responses/', response_list, name='response_list'),
    path('responses/<int:pk>/<str:status>/', change_response_status, name='change_response_status'),
    path('subscribe/', subscribe, name='subscribe'),
    path('newsletters/<int:pk>/send/', send_newsletter, name='send_newsletter'),
    path('accounts/confirm/<str:code>/', confirm_email, name='confirm_email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)