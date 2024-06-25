"""dyoutube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path
from dl import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('login', views.user_login),
    re_path(r'^login/$', views.user_login, name='login'),
    re_path(r'^logout/$', views.user_logout, name='logout'),
    # re_path(r'^logout-then-login/$', 'django.contrib.auth.views.logout_then_login', name='logout_then_login'),

    path('watch', views.watch, name='watch'),
    path('settings', views.settings, name='settings'),
    path('ytdlp-presets', views.ytdlppresets, name='ytdlp-presets'),
    
    path('settingschange', views.settingschange),

    path('search', views.search),
    path('download', views.download),
    path('checkplate', views.checkplate),
    path('startstop', views.startstop),
    path('delete', views.delete),
    path('savepreset', views.savepreset),
    path('deletepreset', views.deletepreset),
]
