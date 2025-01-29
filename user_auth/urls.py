from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'user_auth'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page = 'user_auth:login', template_name=None), name='logout'),
]

