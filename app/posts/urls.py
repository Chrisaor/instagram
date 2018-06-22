from django.urls import path

from posts import views

app_name = 'posts'
urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('<int:pk>/', views.post_detail, name='post-detail'),
]