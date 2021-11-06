from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages


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
            username = form.cleaned_data.get('username')
            messages.success(
                request=request, message=f'Your account for {username} has been created!')
            return redirect('login')
        return render(request=request, template_name='users/register.html', context={
            'form': form
        })


@login_required
def profile(request):
    profile = Profile.objects.get(user_name=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(
                request=request, message=f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile
    }
    user = Profile.objects.get(user_name=request.user)
    print(f'''

        {user}

        ''')
    return render(request=request, template_name='users/profile.html', context=context)
