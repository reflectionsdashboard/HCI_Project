from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from reflections.models import *
from collections import defaultdict
from django.contrib.auth.models import User


@login_required(login_url="/accounts/signin")
def show_dashboard(request):
    user_id = request.user
    user = User.objects.get(username=user_id)
    first_name = user.first_name
    last_name = user.last_name
    student_name = first_name + " " + last_name
    return render(request, "dashboard/dashboard.html", {'student_name': student_name})


def get_reflection_data(request):
    user_id = request.user
    subject_name = request.GET['subject']
    subject = Subject.objects.get(name=subject_name)
    reflections = Reflection.objects.filter(student_handle=user_id, is_pending=False, subject=subject).order_by('id')[:5][::-1]
    total_reflections = Reflection.objects.filter(student_handle=user_id, is_pending=False, subject=subject).count()
    legend = return_topic_legend(reflections)
    return render(request, "dashboard/recent_reflections_table.html", {"reflections": reflections,
                                                                       "legend": legend,
                                                                       "total_reflections": total_reflections})

def get_recent_chart_data(request):
    user_id = request.user
    subject_name = request.GET['subject']
    subject = Subject.objects.get(name=subject_name)
    reflections = Reflection.objects.filter(student_handle=user_id, is_pending=False, subject=subject).order_by('id')[:5][::-1]
    chart_data = return_pie_chart_json(reflections)
    return JsonResponse(chart_data, safe=False)


def get_complete_chart_data(request):
    user_id = request.user
    subject_name = request.GET['subject']
    subject = Subject.objects.get(name=subject_name)
    reflections = Reflection.objects.filter(student_handle=user_id, is_pending=False, subject=subject).order_by('id')
    chart_data = return_pie_chart_json(reflections)
    return JsonResponse(chart_data, safe=False)


def get_bar_chart_data(request):
    user_id = request.user
    subject_name = request.GET['subject']
    chart_data = return_bar_chart_json(user_id, subject_name)
    return JsonResponse(chart_data, safe=False)


def return_topic_legend(reflections):
    topics = [reflection.topic for reflection in reflections if reflection.topic is not None]
    topics = list(set(topics))
    topics.sort(key=lambda topic: topic.id)
    legend = ', '.join(topic.mapping() for topic in topics)
    return legend


def return_pie_chart_json(reflections):
    inaccurate_categories = [reflection.inaccuracy_category.description for reflection in reflections
                             if reflection.inaccuracy_category is not None]
    inaccurate_categories.sort()

    reflection_dict = defaultdict(int)

    for reflection in reflections:
        if reflection.topic is None:
            reflection_dict['Irrelevant'] += 10
        else:
            if reflection.inaccuracy_category is None:
                reflection_dict['Accurate'] += reflection.accuracy
            else:
                reflection_dict[reflection.inaccuracy_category.description] += (10 - reflection.accuracy)
                reflection_dict['Accurate'] += reflection.accuracy

    available_colors = return_available_colors()
    available_border_colors = return_available_border_colors()

    labels = []
    values = []
    background_colors = []
    border_colors = []

    for key in sorted(reflection_dict):
        labels.append(key)
        value = reflection_dict[key]/len(reflections)*10
        values.append(value)
        if key == 'Irrelevant':
            background_colors.append(return_grey_color)
            border_colors.append(return_grey_color)
        elif key == 'Accurate':
            background_colors.append(return_green_color_with_alpha('1'))
            border_colors.append(return_green_color_with_alpha('0.5'))
        else:
            bg_color = available_colors.pop()
            br_color = available_border_colors.pop()
            background_colors.append(bg_color)
            border_colors.append(br_color)

    json = {}
    json['labels'] = labels
    dataset = {}
    dataset['data'] = values
    dataset['backgroundColor'] = background_colors
    dataset['borderColor'] = border_colors
    dataset['borderWidth'] = 1
    json['datasets'] = [dataset]

    return json


def return_bar_chart_json(user_id, subject_name):
    subject = Subject.objects.get(name=subject_name)
    topics = Topic.objects.filter(subject_id=subject).order_by('name')
    reflections = Reflection.objects.filter(student_handle=user_id, is_pending=False, subject=subject)

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
            value = value/total_reflections_dict[key]*10

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
