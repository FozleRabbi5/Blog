from django.urls import path
from . import views

app_name = 'blog_app'

urlpatterns = [
    path('', views.BlogList.as_view(), name='blog_list'),
    path('write/', views.CreateBlog.as_view(), name='create-blog'),
    path('blog_detail/<str:slug>/', views.blog_detail, name='blog_detail'),
    path('like/<int:pk>/', views.liked, name='like_post'),
    path('unlike/<int:pk>/', views.unliked, name='unliked_post'),
    path('myblog/', views.MyBlogs.as_view(), name='myblogs'),
    path('edit/<int:pk>/', views.EditBlog.as_view(), name='edit_blog'),
]
