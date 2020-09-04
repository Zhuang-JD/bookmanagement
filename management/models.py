from django.db import models


# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=128, verbose_name='书籍名称')
    author = models.CharField(max_length=64, verbose_name='作者')
    price = models.FloatField(default=0.0, verbose_name='定价')
    publish_date = models.DateField(null=True, blank=True, verbose_name='出版日期')
    category = models.CharField(max_length=32, default='未分类', verbose_name='书籍分类')

    def __str__(self):
        # 定义__str__方法后，在将模型对象作为参数传递给str()函数时将会调用该方法返回相应的字符串
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=128, verbose_name='图片名称')
    description = models.TextField(default='', verbose_name='图片描述')
    img = models.ImageField(upload_to='image/%Y/%m/%d', verbose_name='图片')
    # 一个图片属于一本书，一本书有多个图片
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='所属书籍')

    def __str__(self):
        return self.name
