from django.shortcuts import render
from .models import Blog, Comment, UserViews, BlogViews
from users.models import User


def HomeView(request):
    posts = Blog.objects.all()
    return render(request=request, template_name='home/home.html', context={'title': 'Home', 'posts': posts})


def render_user(request, param):
    user = User.objects.get(slug=param)
    print(f'user: {user}')
    curr = request.user
    print(f'curr: {curr}')

    try:
        curr_view = UserViews.objects.get(viewer=curr)
        print(f'curr_view: {curr_view}')
    except UserViews.DoesNotExist:
        viewed = UserViews(viewer=curr, viewee=user)
        viewed.save()
        user.views += 1
        user.save()

    posts = Blog.objects.filter(author=user)
    return render(request=request, template_name='home/user.html', context={
        'title': user.user.username,
        'user': user,
        'posts': posts
    })


def render_post(request, param):
    post = Blog.objects.get(slug=param)
    curr = request.user
    print(f'curr: {curr}')

    try:
        curr_view = BlogViews.objects.get(viewer=curr)
        print(f'curr_view: {curr_view}')
    except BlogViews.DoesNotExist:
        viewed = BlogViews(viewer=curr, blog=post)
        viewed.save()
        post.views += 1
        post.save()

    comments = Comment.objects.filter(comment_to_post=post)
    return render(request=request, template_name='home/blogs.html', context={
        'title': post.title,
        'post': post,
        'Comments': comments,
    })
