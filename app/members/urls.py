from django.urls import path

from members import views

app_name = 'members'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('<int:pk>/my_info', views.my_info, name='my-info'),
    path('<int:pk>/user_info', views.user_info, name='user-info'),
    path('<int:pk>/withdraw/', views.withdraw, name='withdraw'),
    path('<int:pk>/follow_toggle', views.follow_toggle, name='follow'),
    path('<int:pk>/user_info/followers', views.follower_list, name='followers'),
    path('<int:pk>/user_info/followings', views.following_list, name='followings')

]
