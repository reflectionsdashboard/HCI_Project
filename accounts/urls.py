from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = "accounts"

urlpatterns = [
    path('', views.sign_in_view, name="signin"),
    path('signup', views.signup_view, name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/signin.html'), name='signin'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='sign out'),

]
