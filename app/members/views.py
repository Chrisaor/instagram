from django.contrib import messages
from django.contrib.auth import authenticate, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# User클래스 자체를 가져올 때는 get_user_model()
# ForeignKey에 User모델을 지정할 때는 settings.AUTH_USER_MODEL

User = get_user_model()

def login_view(request):
    # 1. member.urls <= 'members/'로 include되도록 config.urls모듈에 추가
    # 2. path 구현 (URL : '/members/login/')
    # 3. path와 이 view연결
    # 4. 일단 잘 나오는지 확인
    # 5. 잘 나오면 form 작성
    # 6. POST방식 요청 보내서 request.POST에 요청이 잘 왔는지 확인
    # 7. 받은 username, password값을  HttpResponse에 보여줌
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # print(request.POST)
        # print(username)
        # print(password)
        # result = ''
        # result += f'ID : {username}\n'
        # result += f'PW : {str(password)}\n'
        # return HttpResponse(result)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            print('로그인 전', request.user.is_authenticated)
            login(request, user)
            print('로그인 후', request.user.is_authenticated)
            return redirect('posts:post-list')
        else:
            return redirect('members:login')
    else:
        return render(request, 'members/login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        print('로그아웃!')
        return redirect('index')

def signup(request):
    # errors = list()
    # if request.method == 'POST':
    #     # exists를 사용해서 유저가 이미 존재하면 signup으로 다시 redirect
    #     # 존재하지 않는 경우에만 아래 로직 실행
    #     if not User.objects.filter(username=request.POST['username']).exists():
    #         if request.POST['password1'] == request.POST['password2']:
    #             username = request.POST['username']
    #             password = request.POST['password1']
    #             print(username)
    #             print(password)
    #             user = User.objects.create_user(username = username, password=password)
    #             print('created user: ',user.username)
    #             print('user_password: ',user.password)
    #             user = authenticate(request, username=username, password=password)
    #             print('authenticate', user)
    #             if user is not None:
    #                 print('로그인전',request.user.is_authenticated)
    #                 login(request, user)
    #                 print('로그인후',request.user.is_authenticated)
    #                 return redirect('posts:post-list')
    #             else:
    #                 return redirect('members:login')
    #         else:
    #             print('입력한 비밀번호가 다름')
    #             errors.append('입력한 비밀번호가 다름')
    #             context = {
    #                 'errors':errors,
    #             }
    #             messages.warning(request, ('입력한 비밀번호가 일치하지 않습니다.'))
    #             return render(request, 'members/signup.html', context)
    #     else:
    #         print('유저가 이미 존재함')
    #         # messages.warning(request, ('이미 존재하는 아이디입니다.'))
    #         errors.append('유저가 이미 존재함')
    #         context = {
    #             'errors': errors,
    #             'username': request.POST['username'],
    #             'email':request.POST['email'],
    #             'phone_no':request.POST['phone_no']
    #         }
    #
    #         return render(request, 'members/signup.html', context)
    # return render(request, 'members/signup.html')
    context = {
        'errors': [],
    }
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        context['username'] = username
        context['email'] = email

        if password!=password2:
            context['errors'].append('비밀번호가 다릅니다.')
        if User.objects.filter(username=username).exists():
            context['errors'].append('유저가 이미 존재함')

        if context['errors']:
            return render(request, 'members/signup.html', context)

        User.objects.create_user(username=username, password=password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print('로그인전',request.user.is_authenticated)
            login(request, user)
            print('로그인후',request.user.is_authenticated)
            return redirect('posts:post-list')
        else:
            return redirect('members:login')
    return render(request, 'members/signup.html')
