"""LinkTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import GetIpAddress.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', GetIpAddress.views.index),
    url(r'login.html', GetIpAddress.views.login),
    url(r'proxy_info.html', GetIpAddress.views.proxy_index),
    url(r'agent_info.html', GetIpAddress.views.agent_index),
    url(r'url_info.html', GetIpAddress.views.url_index),
    url(r'add_agent.html', GetIpAddress.views.add_agent),
    url(r'add_url.html', GetIpAddress.views.add_url),
    url(r'delete_agent.html', GetIpAddress.views.delete_agent),
    url(r'delete_url.html', GetIpAddress.views.delete_url),
    url(r'update', GetIpAddress.views.update),
    url(r'task_info.html', GetIpAddress.views.task_info),
    url(r'logout', GetIpAddress.views.logout),
]
