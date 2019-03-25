from django.shortcuts import render, redirect
from .forms import SignInForm, SignUpForm

def sign_in_view(request):
    if request.method == "POST":
        return redirect("dashboard:dashboard")
    else:
        form = SignInForm
        return render(request, "accounts/signin.html", {"form": form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            form.current_user = request.user
            return redirect("accounts:signin")

    else:
        form = SignUpForm
    return  render(request, "accounts/signup.html", {"form": form})

