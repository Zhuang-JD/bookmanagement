import json
import time

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.views.generic import View


# 在顶部要导入我们写的forms模块:from . import forms
# 对于非POST方法发送数据时，比如GET方法请求页面，返回空的表单，让用户可以填入数据；
# 对于POST方法，接收表单数据，并验证；
# 使用表单类自带的is_valid()方法一步完成数据验证工作；
# 验证成功后可以从表单对象的cleaned_data数据字典中获取表单的具体值；
# 如果验证不通过，则返回一个包含先前数据的表单给前端页面，方便用户修改。
# 也就是说，它会帮你保留先前填写的数据内容，而不是返回一个空表！


# 创建验证码
def captcha():
    hashkey = CaptchaStore.generate_key()  # 验证码答案
    image_url = captcha_image_url(hashkey)  # 验证码地址
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    return captcha


# 刷新验证码
def refresh_captcha(request):
    return HttpResponse(json.dumps(captcha()), content_type='application/json')


# 验证验证码
def jarge_captcha(captchaStr, captchaHashkey):
    if captchaStr and captchaHashkey:
        try:
            # 获取根据hashkey获取数据库中的response值
            get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
            if get_captcha.response == captchaStr.lower():  # 如果验证码匹配
                return True
        except:
            return False
    else:
        return False

# https://www.cnblogs.com/-wenli/p/13446543.html 验证码刷新
class IndexView(View):

    def get(self, request):
        hashkey = CaptchaStore.generate_key()  # 验证码答案
        image_url = captcha_image_url(hashkey)  # 验证码地址
        print(hashkey, '-----------', image_url)
        captcha = {'hashkey': hashkey, 'image_url': image_url}

        return render(request, "login1.html", locals())

    def post(self, request):

        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        capt = request.POST.get("captcha", None)  # 用户提交的验证码
        key = request.POST.get("hashkey", None)  # 验证码答案

        try:
            user = models.User.objects.get(name=username)
            print(user)
        except:
            message = '用户不存在！'
            # Python内置了一个locals()函数，它返回当前所有的本地变量字典，我们可以偷懒的将这作为render函数的数据字典参数值，
            # 就不用费劲去构造一个形如{'message':message, 'login_form':login_form}的字典了。
            return render(request, 'login1.html', locals())

        # if user.captcha != captcha:
        #     message = '请重新输入验证码！'
        #     login_form.captcha.error = True
        #     return render(request, 'login/login.html', locals())

        if not user.has_confirmed:
            message = '该用户还未经过邮件确认！！！'
            return render(request, 'login1.html', locals())
        if jarge_captcha(capt, key):
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                print('登录成功')
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login1.html', locals())
        else:
            message = '验证码错误'
            return render(request, 'login1.html', locals())


# 密码使用哈希加密
import hashlib


def hash_code(s, salt='zjd'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


# 创建确认码对象
import datetime


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user, )
    return code


# 创建账号邮箱发送邮件方法

from django.conf import settings


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '注册确认邮件'

    text_content = '''============感谢注册================'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                    这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# Create your views here.

def index(request):
    return render(request, 'login/index.html')


def login2(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    # if request.is_ajax():  # 请求ajax则返回新的image_url和key
    #     result = dict()
    #     result['key'] = CaptchaStore.generate_key()
    #     result['image_url'] = captcha_image_url(result['key'])
    #     return JsonResponse(result)
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写内容！'
        if login_form.is_valid():
            # 验证成功后可以从表单对象的cleaned_data数据字典中获取表单的具体值
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            # if username.strip() and password:  # 确保用户名和密码都不为空
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在！'
                # Python内置了一个locals()函数，它返回当前所有的本地变量字典，我们可以偷懒的将这作为render函数的数据字典参数值，
                # 就不用费劲去构造一个形如{'message':message, 'login_form':login_form}的字典了。
                return render(request, 'login/login.html', locals())

            # if user.captcha != captcha:
            #     message = '请重新输入验证码！'
            #     login_form.captcha.error = True
            #     return render(request, 'login/login.html', locals())

            if not user.has_confirmed:
                message = '该用户还未经过邮件确认！'
                return render(request, 'login/login.html', locals())

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())

    # 对于POST方法，接收表单数据，并验证；
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())

                # 判断是否为同个邮箱
                # 尝试过没有下面的语句，同个邮箱报错
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)
                message = '请前往邮箱确认！'

                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect('/login/')
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '邮件过期,请重新注册'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账号登录'
        return render(request, 'login/confirm.html', locals())


def book_detail(request):
    # bb = 0
    # dd = datetime.datetime.now() + datetime.timedelta(seconds=1)
    # while True:
    #     aa = datetime.datetime.now()
    #     if (aa > dd):
    #         dd = aa + datetime.timedelta(seconds=1)
    #         bb += 1
    #         print(bb)
    #         if bb > 20:
    #             break
    numlist = range(0, 101)
    return render(request, 'login/test1.html', locals())
