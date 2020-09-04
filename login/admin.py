from django.contrib import admin
from . import models
from django.apps import AppConfig


# Register your models here.
# class Username(AppConfig):
#     verbose_name = '登录'


admin.site.register(models.User)
admin.site.register(models.ConfirmString)
