from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.shortcuts import redirect
from . import forms, models
from django.http import HttpResponseRedirect

# Create your views here.
from .models import Image, Book


def add_book(request):
    if not request.session.get('is_login', None):
        return redirect('index/')
    if request.method == 'POST':
        add_book_form = forms.Add_book(request.POST)
        message = "请检查填写的内容！"
        if add_book_form.is_valid():
            name = add_book_form.cleaned_data.get('name')
            author = add_book_form.cleaned_data.get('author')
            price = add_book_form.cleaned_data.get('price')
            publish_date = add_book_form.cleaned_data.get('publish_date')
            category = add_book_form.cleaned_data.get('category')

            new_book = models.Book()
            new_book.name = name
            new_book.author = author
            new_book.price = float(price)
            new_book.publish_date = publish_date
            new_book.category = category
            new_book.save()

            return redirect('index/')
        else:
            return render(request, 'management/add_book.html', locals())
    add_book_form = forms.Add_book()
    return render(request, 'management/add_book.html', locals())


def add_img(request):
    if not request.session.get('is_login', None):
        return redirect('index/')
    if request.method == 'POST':
        add_img_form = forms.UploadFiledForm(request.POST, request.FILES)
        message = "请检查填写的内容！"
        if add_img_form.is_valid():
            name = add_img_form.cleaned_data.get('name')
            description = add_img_form.cleaned_data.get('description')
            file = add_img_form.cleaned_data.get('file')
            book = add_img_form.cleaned_data.get('book')
            # 文件格式判读
            # 创建新对象一般用try

            new_img = Image(name=name, description=description, img=file, book=book)
            new_img.save()

            return redirect('index/')
            # return HttpResponseRedirect(reversed('login:index'))
        else:
            return render(request, 'management/add_img.html', locals())
    add_img_form = forms.UploadFiledForm()
    return render(request, 'management/add_img.html', locals())


def book_list(request, category='all'):
    category_list = Book.objects.values_list('category', flat=True).distinct()
    if Book.objects.filter(category=category).count() == 0:
        category = 'all'
        books = Book.objects.all()
    else:
        books = Book.objects.filter(category=category)

    paginator = Paginator(books, 5)  # 进行分页操作，每次５个对象》
    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {
        'active_menu': 'view_book',
        'category_list': category_list,
        'query_category': category,
        'book_list': books
    }
    return render(request, 'management/book_list.html', context)


def book_detail(request, book_id=1):
    try:
        book = Book.objects.get(pk=book_id)
    except:
        return HttpResponseRedirect(reversed('management:book_list', args=('all',)))
    return render(request,'management/book_detail.html',locals())
