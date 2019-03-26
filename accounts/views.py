from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import SignInForm, SignUpForm


def sign_in_view(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect("expert:expert")
            else:
                return redirect("dashboard:dashboard")
    else:
        form = SignInForm()

    return render(request, "accounts/signin.html", {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("dashboard:dashboard")
    else:
        form = SignUpForm()

    print(form.errors)

    return render(request, "accounts/signup.html", {'form': form})


def signout_view(request):
    logout(request)
    return redirect("accounts:signin")

