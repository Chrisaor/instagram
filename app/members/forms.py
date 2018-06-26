from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from members.views import User

User = get_user_model()

class SignupForm(forms.Form):
    username = forms.CharField(label='아이디', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))
    password = forms.CharField(label='패스워드', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
        }
    ))
    password2 = forms.CharField(label='패스워드 확인', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
        }
    ))
    email = forms.EmailField(label='이메일', widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    def clean_username(self):

        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('아이디가 이미 존재합니다')
        return username


    def clean(self):
        super().clean()
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:

            self.add_error('password2','비밀번호가 다릅니다')
        return self.cleaned_data

    def signup(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        return user


