"""dalyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include

from goods.views import *
from django.contrib.auth.decorators import login_required

# /accounts/login/ 没有登录的话默认是找这个路径

urlpatterns = [
    # 为啥后面必须加/
    path('admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    url('^user/', include('user.urls', namespace='user')),
    url('^goods/', include('goods.urls', namespace='goods')),
    url('^order/', include('order.urls', namespace='order')),
    url('^cart/', include('cart.urls', namespace='cart')),
    # login_required装饰器做法
    # url('^$', login_required(index.as_view())),
    url('^$', index.as_view()),

]
