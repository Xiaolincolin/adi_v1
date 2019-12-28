"""adi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from apps.judge.views import ClassifyView, FormView, StatisticsView, WechatView
from apps.users.views import LoginView, LogoutView, TmpView
from django.conf.urls import url

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TmpView.as_view(), name="tmp"),
    url(r'^login$', LoginView.as_view(), name="login"),
    url('^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^media/$', ClassifyView.as_view(), name="judge"),
    url(r'^data/$', FormView.as_view(), name="data"),
    url(r'^fx/$', StatisticsView.as_view(), name="fx"),
    url(r'^wechat/$', WechatView.as_view(), name="wechat")
]
