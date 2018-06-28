from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import PostCreate, PostModelForm
from .models import Post, Comment, PostLike

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
            'form':form,
        }
        return render(request, 'posts/post_create.html',context)


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
        'form':form,
    }
    return render(request, 'posts/post_create.html', context)


@require_POST
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied('지울 권한이 없습니다')
    post.delete()
    return redirect('posts:post-list')


def comment_create(request, pk):

    if request.method == 'POST':
        Comment.objects.create(
            user=request.user,
            post=Post.objects.get(pk=pk),
            comment=request.POST['comment'],
        )
        return redirect('posts:post-list')

def post_like(request, pk):
    if request.method == 'POST':
        PostLike.objects.create(
            user=request.user,
            post=Post.objects.get(pk=pk)
        )
    return redirect('posts:post-list')
