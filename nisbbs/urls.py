"""nisbbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include,url
from django.contrib import admin
from wwrequests import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^wwrequests/',include('wwrequests.urls')),
    url(r'^admin/', admin.site.urls),
    url(
        '^change-password/',
        auth_views.password_change,
        {'template_name': 'registration/change-password.html',
         'post_change_redirect':'/'}
    ),
    url('^', include('django.contrib.auth.urls')),
    url(r'^regist/',views.regist,name = 'regist'),
    url(r'^$', views.view),
]
