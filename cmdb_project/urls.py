"""cmdb_project URL Configuration

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
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from cmdb import rest_urls,urls as asset_urls
from cmdb_project import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(rest_urls) ),
    url(r'^asset/',include('cmdb.urls')),
    url(r'^$',views.index,name="dashboard"),
    url(r'^login/$',views.acc_login,name='login'),
    url(r'^logout/$',views.acc_logout,name='logout'),

]
