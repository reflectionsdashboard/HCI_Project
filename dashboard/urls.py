from django.urls import path
from . import views
from dashboard.views import get_reflection_data, get_recent_chart_data, \
    get_complete_chart_data, get_legend_data, get_bar_chart_data

app_name = "dashboard"

urlpatterns = [
    path('', views.show_dashboard, name="dashboard"),
    path('api/reflection/data', get_reflection_data, name='reflection-data'),
    path('api/recent/chart/data', get_recent_chart_data, name='recent-chart-data'),
    path('api/complete/chart/data', get_complete_chart_data, name='complete-chart-data'),
    path('api/legend/data', get_legend_data, name='legend-data'),
    path('api/bar/chart/data', get_bar_chart_data, name='bar-chart-data'),

]
