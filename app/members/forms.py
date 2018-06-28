from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from members.views import User

User = get_user_model()

class SignupForm(forms.Form):
    img_profile = forms.ImageField(
        label='프로필 사진',
        widget=forms.ClearableFileInput(
            attrs={
                'class':'form-control',
            },
        )
    )

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

    introduce = forms.CharField(label='소개', widget=forms.Textarea(
        attrs={
            'class':'form-control',
        }
    ))
    gender = forms.CharField(
        label='성별',
        widget=forms.Select(
            attrs={
                'class':'form-control',
            },
            choices=User.CHOICE_GENDER,
        )
    )
    site = forms.CharField(
        label='사이트', widget=forms.TextInput(
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
        fields = [
            'username',
            'email',
            'password',
            'gender',
            'img_profile',
            'introduce',
            'site'
        ]
        # create_user_dict = {}
        # for field in fields:
        #     create_user_dict[field]=self.cleaned_data[field]
        #
        # print(create_user_dict)

        # create_user_dict = {key : value for key, value in self.cleaned_data.items() if key in fields}
        # def in_fields(item):
        #     return item[0] in fields
        #
        # result = filter(in_fields, self.cleaned_data.items())
        # for item in result:
        #     print(item)
        #     print(type(item))

        create_user_dict = dict(filter(lambda item: item[0] in fields, self.cleaned_data.items()))
        # print(create_user_dict)
        # print(self.cleaned_data)
        # self.cleaned_data.pop('password2')
        # print(self.cleaned_data)
        user = User.objects.create_user(**create_user_dict)
        # img_profile = self.cleaned_data['img_profile']
        # username = self.cleaned_data['username']
        # email = self.cleaned_data['email']
        # password = self.cleaned_data['password']
        # introduce = self.cleaned_data['introduce']
        # gender = self.cleaned_data['gender']
        #
        # user = User.objects.create_user(
        #     img_profile=img_profile,
        #     username=username,
        #     email=email,
        #     password=password,
        #     introduce=introduce,
        #     gender=gender,
        # )
        return user


