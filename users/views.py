from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required


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
    return render(request=request, template_name='users/profile.html', )
