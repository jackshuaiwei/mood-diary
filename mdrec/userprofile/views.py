import hashlib
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm, UserCreateForm
from django.contrib.auth import authenticate, login, logout
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from .models import ConfirmString
from record.models import Record
from django.core.paginator import Paginator


class UserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


def hash_code(s, salt='mood'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username, now)
    ConfirmString.objects.create(code=code, user=user, )
    return code


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自心情日记的注册确认邮件'

    text_content = '''感谢注册心情日记，记录您美好的一天，带给您美好的回忆！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/userprofile/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                    感谢注册心情日记，记录您美好的一天，带给您美好的回忆！
                    </p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                id = user.id
                return redirect('userprofile:center', id=id)
            else:
                return HttpResponse("账号或密码输入错误!")
        else:
            return HttpResponse("账号和密码输入不合法!")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请求方式不允许")


def user_register(request):
    messqge = "Welcome!"
    if request.method == 'POST':
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.email = user_register_form.cleaned_data.get('email')
            new_user.is_active = False
            new_user.save()
            # login(request, new_user)
            # return redirect('record:index')

            code = make_confirm_string(new_user)
            send_email(user_register_form.cleaned_data.get('email'), code)
            message = '请前往邮箱进行确认！'
            return redirect('userprofile:login')
        else:
            return render(request, 'userprofile/register.html', {"form": user_register_form, "messqge": messqge})
    elif request.method == "GET":
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form, "messqge": messqge}
        return render(request, 'userprofile/register.html', context)


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'userprofile/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'userprofile/confirm.html', locals())
    else:
        confirm.user.is_active = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'userprofile/confirm.html', locals())

@login_required(login_url='/userprofile/login/')
def user_center(request, id):
    if request.user.id != id:
        return HttpResponse("你没有权限访问别人的主页")
    else:
        record_list = Record.objects.filter(user_id=id)
        paginator = Paginator(record_list,3)
        page = request.GET.get('page')
        records = paginator.get_page(page)

        context = {
            "record":records

        }
        return render(request, 'userprofile/usercenter.html', context)

@login_required(login_url='/userprofile/login/')
def user_create(request, id):
    if request.user.id != id:
        return HttpResponse("你没有权限访问别人的主页")
    else:
        if request.method == "POST":
            user_create_form = UserCreateForm(request.POST, request.FILES)
            if user_create_form.is_valid():
                data = user_create_form.cleaned_data
                new_record = user_create_form.save(commit=False)
                new_record.user_id = int(id)
                new_record.save()
                return redirect('userprofile:center',id=id)
            else:
                return HttpResponse("您输入的数据不合法，请检查后输入")

        elif request.method == 'GET':
            user_create_form = UserCreateForm()
            context = {
                "form":user_create_form,
            }
            return render(request, 'userprofile/create.html',context)
        else:
            return HttpResponse("您的请求方式有误")


def user_logout(request):
    logout(request)
    return redirect('record:index')


