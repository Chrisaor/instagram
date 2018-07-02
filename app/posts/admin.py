from django.contrib import admin

from posts.models import Post, Comment, PostLike

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostLike)