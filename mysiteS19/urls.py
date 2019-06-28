"""mysiteS1901 URL Configuration

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

from myapp import views
from django.urls import include, path
from django.conf.urls import url
from django.contrib import admin

#app_name = 'myapp'

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^myapp/index', views.index, name='index'), #beginning; end
    url('myapp/about',views.about, name='about'),
    url(r'^myapp/(?P<cat_no>\d)+',views.detail, name='outcome'),
    url(r'myapp/products/', views.products, name='product'),
    url(r'myapp/place_order', views.place_order, name='order'),
    url(r'^myapp/product/(?P<prod_id>\d)+', views.productdetail, name='productdetail'),
    url(r'^myapp/login/', views.user_login, name='login'),
    url(r'^myapp/logout/', views.user_logout, name='logout'),
    url(r'^myapp/myorders/', views.myorders, name='myorders'),
    url(r'^myapp/register/', views.register, name = 'register')
]