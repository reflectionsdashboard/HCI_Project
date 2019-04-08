from django.urls import path
from . import views
from dashboard.views import get_reflection_data, \
    get_bar_chart_data

app_name = "dashboard"

urlpatterns = [
    path('', views.show_dashboard, name="dashboard"),
    path('api/reflection/data', get_reflection_data, name='reflection-data'),
    path('api/bar/chart/data', get_bar_chart_data, name='bar-chart-data'),

]
