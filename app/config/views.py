from django.contrib.auth import logout
from django.shortcuts import redirect


def index(request):
    return redirect('posts:post-list')

