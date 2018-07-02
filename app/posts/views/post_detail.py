from django.contrib.auth import get_user_model
from django.shortcuts import render

from ..models import Post

all = (
    'post_detail',
)

User = get_user_model()
def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)