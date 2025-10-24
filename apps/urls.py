from django.urls import path

from apps import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index_page'),
    path('profile/', views.ProfileView.as_view(), name='profile_page'),
    path('users/', views.UserListView.as_view(), name='user_list_page'),
    path('posts/', views.UserPostsView.as_view(), name='user_posts_page'),
    path('auth/signup/', views.SignupView.as_view(), name='signup_page'),
    path('auth/login/', views.LoginView.as_view(), name='login_page'),
    path('auth/logout/', views.Logout.as_view(), name='logout_view'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update_view'),
]