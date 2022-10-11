from django.urls import path

from django.http import HttpResponse

from . import views

app_name = 'login_app'

urlpatterns = [
    path('sign_up/', views.sign_up, name='sign_up'),
    path('', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('profile/', views.profile, name='profile'),
    path('changeprofile', views.user_change, name='user_change'),
    path('password/', views.password_change, name='password_change'),
    path('profile-pic/', views.add_pro_pic, name='profile-picture'),
    path('change-pic/', views.change_profile, name='change-profile-pic'),
]
