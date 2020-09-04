from django import forms

from management.models import Book


class Add_book(forms.Form):
    name = forms.CharField(label="书名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.CharField(label="作者", max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.FloatField(label="价格", widget=forms.TextInput(attrs={'class': 'form-control'}))
    publish_date = forms.DateField(label="出版日期", widget=forms.DateInput(attrs={'type': 'date'}))
    category = forms.CharField(label='书籍分类', max_length=32)


class UploadFiledForm(forms.Form):
    name = forms.CharField(label='图片名称', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='图片描述', max_length=512, widget=forms.TextInput(attrs={'class': 'form-control'}))
    file = forms.FileField(label='图片上传')
    book = forms.ModelChoiceField(label='所属书籍',queryset=Book.objects.all())

