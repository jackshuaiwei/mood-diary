from django import forms
from record.models import Record
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '用户名 | 邮箱'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '密码'}))
    # email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': '邮箱'}))


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': '用户名'}))
    password = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': '密码'}))
    password2 = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': '确认密码'}))
    email = forms.EmailField(max_length=20, widget=forms.TextInput(attrs={'placeholder': '邮箱'}))

    class Meta:
        model = User
        fields = ['username','email']


    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError('密码输入不一致，请重新输入')

    def clean_username(self):
        data = self.cleaned_data
        ret = User.objects.filter(username=data.get('username')).exists()
        if ret:
            raise forms.ValidationError('用户名已存在！')
        else:
            return data.get('username')

    def clean_email(self):
        data = self.cleaned_data
        ret = User.objects.filter(email=data.get('email')).exists()
        if ret:
            raise forms.ValidationError('该邮箱已被注册')
        else:
            return data.get('email')


    def get_errors(self):
        errors = self.errors.get_json_data()
        new_errors = {}
        messages = []
        for key,message_dicts in errors.items(): # key是表单字段， message_dicts是字段对应的值（一个list，里面保存错误的字典）
            for message in message_dicts:
                messages.append(message['message'])  # message键对应的值存储
            # new_errors[key] = messages  # 保存表单字段的message键对应的值
        # return new_errors
        if messages:
            return messages[0]
        else:
            return "Welcome!"


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('title','content','song_url')

