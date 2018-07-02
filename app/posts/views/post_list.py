from django.contrib.auth import get_user_model
from django.shortcuts import render

from ..models import Post

all = (
    'post_list'
)

User = get_user_model()
def post_list(request):
    posts = Post.objects.all()
    try:
        following = request.user.following
    except AttributeError:
        following = []
    context = {
        'posts': posts,
        'following':following,
    }
    return render(request, 'posts/post_list.html', context)