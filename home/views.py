from django.shortcuts import render, redirect
from .models import Blog, Comment, UserViews, BlogViews
from users.models import Profile
from .forms import BlogForm
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required


class PostListView(ListView):
    template_name = 'home/home.html'
    context_object_name = 'posts'
    model = Blog
    ordering = ['-date_posted']


@login_required
def render_user(request, param):
    profile = Profile.objects.get(slug=param)
    print(f'user: {profile}')
    curr = request.user
    print(f'curr: {curr} to {profile}, {type(str(curr))}')

    # try:
    #     curr_view = UserViews.objects.get(viewer=curr)
    #     print(f'curr_view: {curr_view}')
    # except UserViews.DoesNotExist:
    #     viewed = UserViews(viewer=curr, viewee=user)
    #     viewed.save()
    #     print(f'Old No. of Views: {user.views}')
    #     user.views += 1
    #     print(f'New No. of Views: {user.views}')
    #     user.save()

    if not UserViews.objects.filter(viewer=str(curr)).filter(viewee=profile).exists() and str(curr) != str(profile.user.username):
        viewed = UserViews(viewer=curr, viewee=profile)
        viewed.save()
        print(f'Old No. of Views: {profile.views}')
        profile.views += 1
        print(f'New No. of Views: {profile.views}')
        profile.save()

    posts = Blog.objects.filter(author=profile)
    return render(request=request, template_name='home/user.html', context={
        'profile': profile,
        'posts': posts
    })


@login_required
def render_post(request, param):
    post = Blog.objects.get(slug=param)
    curr = request.user
    print(f'curr: {curr} to {post}, {type(str(curr))}')

    # try:
    #     curr_view = BlogViews.objects.get(viewer=curr)
    #     print(f'curr_view: {curr_view}')
    # except BlogViews.DoesNotExist:
    #     viewed = BlogViews(viewer=curr, blog=post)
    #     viewed.save()
    #     print(f'Old No. of Views: {post.views}')
    #     post.views += 1
    #     print(f'New No. of Views: {post.views}')
    #     post.save()

    if not BlogViews.objects.filter(viewer=str(curr)).filter(blog=post).exists() and str(curr) != str(post.author.user.username):
        viewed = BlogViews(viewer=curr, blog=post)
        viewed.save()
        print(f'Old No. of Views: {post.views}')
        post.views += 1
        print(f'New No. of Views: {post.views}')
        post.save()

    comments = Comment.objects.filter(comment_to_post=post)
    return render(request=request, template_name='home/blogs.html', context={
        'post': post,
        'Comments': comments,
    })


@login_required
def write_blog(request):
    profile = Profile.objects.get(user_name=str(request.user))
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = Blog(author=profile, title=form.cleaned_data.get(
                'title'), content=form.cleaned_data.get('content'))
            blog.save()
            return redirect('home')
        else:
            form = BlogForm(request.POST)
    else:
        form = BlogForm()
        return render(request=request, template_name='home/blog_form.html', context={'form': form})
