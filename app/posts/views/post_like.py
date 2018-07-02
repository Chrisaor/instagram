from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from ..models import Post, PostLike

all = (
    'post_like',
)

User = get_user_model()
def post_like(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        try:
            post_like = PostLike.objects.get(user=request.user, post=post)
            post_like.delete()
        except PostLike.DoesNotExist:
            PostLike.objects.create(user=request.user, post=post)

    return redirect('posts:post-list')