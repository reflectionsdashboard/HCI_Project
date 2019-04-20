from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from reflections.models import *
from collections import defaultdict
from django.contrib.auth.models import User


@login_required(login_url="/accounts/signin")
def show_dashboard(request):
    user_id = request.user
    user = User.objects.get(username=user_id)

    if user.is_staff or user.is_superuser:
        student_name = 'Expert'
    else:
        first_name = user.first_name
        last_name = user.last_name
        student_name = first_name + " " + last_name

    computer_organization = Subject.objects.get(name='Computer Organization')
    data_structures = Subject.objects.get(name='Data Structures')

    return render(request, "dashboard/dashboard.html", {'student_name': student_name,
                                                        'computer_organization': computer_organization.id,
                                                        'data_structures': data_structures.id})


def get_reflection_data(request):
    #Canvas Reflections
    user_id = request.user
    user = User.objects.get(username=user_id)
    subject_id = request.GET['subject_id']

    if user.is_staff or user.is_superuser:
    # if True:
        reflections = Reflection.objects.filter(is_pending=False, subject_id=subject_id).order_by('id')[:5][::-1]
        total_reflections = Reflection.objects.filter(is_pending=False, subject_id=subject_id).count()
    else:
        reflections = Reflection.objects.filter(student_handle=user_id, is_pending=False, subject_id=subject_id).order_by('id')[:5][::-1]
        total_reflections = Reflection.objects.filter(student_handle=user_id, is_pending=False, subject_id=subject_id).count()

    legend = return_topic_legend(reflections)
    return render(request, "dashboard/recent_reflections_table.html", {"reflections": reflections,
                                                                       "legend": legend,
                                                                       "total_reflections": total_reflections})


def get_bar_chart_data(request):
    user_id = request.user
    subject_id = request.GET['subject_id']
    chart_data = return_bar_chart_json(user_id, subject_id)
    return JsonResponse(chart_data, safe=False)


def return_topic_legend(reflections):
    topics = [reflection.topic for reflection in reflections if reflection.topic is not None]
    topics = list(set(topics))
    topics.sort(key=lambda topic: topic.id)
    legend = ', '.join(topic.mapping() for topic in topics)
    return legend


def return_bar_chart_json(user_id, subject_id):
    #Column Chart
    user = User.objects.get(username=user_id)
    topics = Topic.objects.filter(subject_id=subject_id).order_by('name')

    if user.is_staff or user.is_superuser:
    # if True:
        reflections = Reflection.objects.filter(is_pending=False, subject_id=subject_id)
    else:
        reflections = Reflection.objects.filter(student_handle=user_id, is_pending=False, subject_id=subject_id)

    labels = []
    values = []
    background_colors = []
    border_colors = []

    accuracy_dict = defaultdict(int)
    total_reflections_dict = defaultdict(int)

    for topic in topics:
        accuracy_dict[topic] = 0
        total_reflections_dict[topic] = 0

    available_colors = return_available_colors()
    available_border_colors = return_available_border_colors()

    for reflection in reflections:
        reflection_topic = reflection.topic
        if accuracy_dict.__contains__(reflection_topic):
            accuracy_dict[reflection_topic] += reflection.accuracy
            total_reflections_dict[reflection_topic] += 1

    for key in accuracy_dict:
        labels.append(key.name)

        value = accuracy_dict[key]
        if total_reflections_dict[key] > 0:
            value = round(value/total_reflections_dict[key]*10, 2)

        values.append(value)
        bg_color = available_colors.pop()
        br_color = available_border_colors.pop()
        background_colors.append(bg_color)
        border_colors.append(br_color)

    json = {}
    json['labels'] = labels
    dataset = {}
    dataset['label'] = 'Accuracy'
    dataset['data'] = values
    dataset['backgroundColor'] = background_colors
    dataset['borderColor'] = border_colors
    dataset['borderWidth'] = 1
    json['datasets'] = [dataset]

    return json


def return_available_colors():
    available_colors = ['rgba(255, 99, 132, 0.5)', 'rgba(54, 162, 235, 0.5)', 'rgba(51, 153, 255, 0.5)'
        , 'rgba(153, 102, 255, 0.5)', 'rgba(255, 159, 64, 0.5)']
    return available_colors


def return_available_border_colors():
    available_border_colors = ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(51, 153, 255, 1)',
                               'rgba(153, 102, 255, 1)', 'rgba(255, 159, 64, 1)']

    return available_border_colors


def return_grey_color():
    return 'rgb(150, 150, 150, 0.2)'


def return_green_color_with_alpha(alpha):
    return 'rgba(0, 204, 153, '+alpha+')'
