from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from . import forms
# Create your views here.


def sign_up(request):
    form = forms.Sign_upForm()
    registered = False
    if request.method == 'POST':
        form = forms.Sign_upForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            registered = True

    diction = {'form': form, 'registered': registered}
    return render(request, 'login_app/sign_up.html', context=diction)


def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))

    diction = {'form': form}
    return render(request, 'login_app/log_in.html', context=diction)


@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_app:log_in'))


@login_required
def profile(request):
    return render(request, 'login_app/profile.html', context={})


@login_required
def user_change(request):
    current_user = request.user
    form = forms.profileChangeForm(instance=current_user)

    if request.method == 'POST':
        form = forms.profileChangeForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            form = forms.profileChangeForm(instance=current_user)
    return render(request, 'login_app/changeprofile.html', context={'form': form})


@login_required
def password_change(request):
    current_user = request.user
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()

    diction = {'form': form, 'msg': 'password has been changed successfully'}
    return render(request, 'login_app/change_pass.html', context=diction)


@login_required
def add_pro_pic(request):
    form = forms.ProfilePic()

    if request.method == 'POST':
        form = forms.ProfilePic(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('login_app:profile'))
    return render(request, 'login_app/pro_pic.html', context={'form': form})


@login_required
def change_profile(request):
    form = forms.ProfilePic(instance=request.user.user_profile)
    if request.method == 'POST':
        form = forms.ProfilePic(
            request.POST, request.FILES, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login_app:profile'))
    return render(request, 'login_app/pro_pic.html', context={'form': form})
