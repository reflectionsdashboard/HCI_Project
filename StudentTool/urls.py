from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from accounts import views

urlpatterns = [
    # path(r'', views.sign_in_view, name='home'),
    path('', include('expert.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('expert/', include('expert.urls')),
]

urlpatterns += staticfiles_urlpatterns()
