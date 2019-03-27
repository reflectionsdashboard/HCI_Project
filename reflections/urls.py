from django.urls import path
from .views import show_reflections_view, get_reflection_data, get_subject_data, get_topic_data

app_name = "reflections"

urlpatterns = [
    path('', show_reflections_view, name="reflections"),
    path('api/reflections/data', get_reflection_data, name='reflection-data'),
    path('api/subject/data', get_subject_data, name='subject-data'),
    path('api/topic/data', get_topic_data, name='topic-data'),

]
