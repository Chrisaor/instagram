from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ..forms import PostModelForm, PostCreate

all = (
    'post_create',
    'post_create_with_form',
)

User = get_user_model()

def post_create(request):
    # PostModelForm을 사용
    # form = PostModelForm(request.POST, request.FILES)
    # form.save()
    if request.method == 'POST':
        print('POST')
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostModelForm()
        context = {
            'form': form,
        }
        return render(request, 'posts/post_create.html', context)

    @login_required
    def post_create_with_form(request):
        if request.method == 'POST':
            form = PostCreate(request.POST, request.FILES)
            print(request.POST, request.FILES)
            if form.is_valid():
                form.create_post(request.user)
                return redirect('index')
            print('valid false')
        else:
            form = PostCreate()

        context = {
            'form': form,
        }
        return render(request, 'posts/post_create.html', context)