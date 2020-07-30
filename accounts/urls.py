from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('', views.user_index, name='user_index'),
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('active/', views.user_active, name='user_active'),
    path('verify/<str:email>/<str:code>/', views.user_verify, name='user_verify'),
    path('resend/', views.resend_code, name='resend_code'),
    path('forget/', views.user_forget, name='user_forget'),
    path('change-password/', views.user_change_password, name='user_change_password_reset'),
    path('change-password/<str:email>/<str:code>/', views.user_change_password, name='user_change_password'),
    path('logout/', views.user_logout, name='user_logout'),
]

# path('active/', views.user_active, name='user_active'),
