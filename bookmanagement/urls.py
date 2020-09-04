"""bookmanagement URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from bookmanagement import settings
from login import views
from management import views as ve
from django.urls import include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from  login.views import IndexView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login1/', views.login2, name='login2'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('captcha/', include('captcha.urls')),
    # path('^ajax_val/', views.ajax_val, name='ajax_val'),
    path('refresh_captcha/',views.refresh_captcha,name='refresh_captcha'),
    path('login/',IndexView.as_view(),name='login'),                  #get与post请求路径
    path('confirm/', views.user_confirm),
    path('add_book/', ve.add_book, name='add_book'),
    path('add_book/index/', views.index),
    path('add_img/', ve.add_img, name='add_img'),
    path('add_img/index/', views.index),
    path('book_list/', ve.book_list, name='book_list'),
    path('book_list/<str:category>/', ve.book_list, name='book_list'),
    path('book_detail/<book_id>/',ve.book_detail,name='book_detail'),
    path('test/',views.book_detail,name='test'),

    # path('book_detail/',ve.book_detail,name='book_detail'),
    # path('book_detail/.*',ve.book_detail,name='book_detail'),
]

# admin后台打开
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
