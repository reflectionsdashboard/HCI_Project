from django.urls import path
from . import views

app_name = "expert"

urlpatterns = [
    path('', views.show_expert_view, name="expert"),
]
