from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserProfileForm
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def profile(request):
    profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'user': request.user,
    })
