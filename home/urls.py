from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('profile/<slug:param>', views.render_user, name='blog-user'),
    path('posts/<slug:param>', views.render_post, name='blog-post'),
    path('posts/new/', views.write_blog, name='blog-write')
]
