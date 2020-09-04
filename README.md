## 这是一个用户登录和注册的书城项目
## 可以添加图书和图片
## 这是一个可重用的登录和注册APP


## 简单的使用方法：


创建虚拟环境
使用pip安装第三方依赖
运行migrate命令，创建数据库和数据表
运行python manage.py runserver启动服务器


路由设置：


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