from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from home.models import Blog
from .models import Profile


class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request=request, template_name='users/register.html', context={
            'form': form
        })

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request=request, template_name='users/register.html', context={
            'form': form
        })


@login_required
def profile(request):
    user = Profile.objects.get(user_name=request.user)
    print(f'''

        {user}

        ''')
    post = []
    if Blog.objects.filter(author=user).exists():
        post = Blog.objects.get(author=user)
    return render(request=request, template_name='users/profile.html')
