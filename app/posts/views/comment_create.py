from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from ..models import Comment, Post

all = (
    'comment_create'
)

User = get_user_model()


def comment_create(request, pk):
    if request.method == 'POST':
        Comment.objects.create(
            user=request.user,
            post=Post.objects.get(pk=pk),
            comment=request.POST['comment'],
        )
        return redirect('posts:post-list')
