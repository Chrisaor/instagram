from django.conf import settings
from django.db import models

from members.models import User


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='post', blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    like_users_at_post = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        # 내가 좋아요를 누른 Post목록
        related_name='like_posts',
    )
    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.author}님의 게시물'

    @property
    def like_users(self):
        pl_qs = PostLike.objects.filter(post=self)
        users = list()
        for pl in pl_qs:
            users.append(pl.user)
        return users


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    comment = models.CharField(max_length=200)

    class Meta:
        ordering = ['-comment']

    def __str__(self):
        return f'{self.user}님의 댓글'


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)



