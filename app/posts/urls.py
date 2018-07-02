from django.urls import path

from posts import views

app_name = 'posts'
urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('<int:pk>/', views.post_detail, name='post-detail'),
    path('post_create/', views.post_create, name='post-create'),
    path('<int:pk>/post_delete/', views.post_delete, name='post-delete'),
    path('<int:pk>/comment_create/', views.comment_create, name='comment-create'),
    path('<int:pk>/post_like', views.post_like, name='post-like'),

]