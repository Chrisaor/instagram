from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from posts.forms import PostCreate
from posts.models import Post

User = get_user_model()

def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts':posts,
    }
    return render(request, 'posts/post_list.html', context)

def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    context = {
        'post':post,
    }
    return render(request, 'posts/post_detail.html', context)

@login_required(login_url='/members/login')
def post_create(request):
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
        'form':form,
    }
    return render(request, 'posts/post_create.html', context)


def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST' and request.user==post.author:
        post.delete()
        return redirect('index')
    return render(request, 'members/login.html')