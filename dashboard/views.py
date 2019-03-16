from django.shortcuts import render
from reflections.models import *
from collections import defaultdict

import json


def show_dashboard(request):
    reflections = Reflection.objects.filter(is_pending=False).order_by('id')[:5][::-1]
    legend = return_topic_legend(reflections)
    chart_data = return_json(reflections)
    json_chart_data = json.dumps(chart_data, ensure_ascii=False, sort_keys=True, indent=4)
    return render(request, "dashboard/dashboard.html", {"reflections": reflections, "legend": legend, "chart_data": json_chart_data})


def return_topic_legend(reflections):
    topics = [reflection.topic for reflection in reflections if reflection.topic is not None]
    topics = list(set(topics))
    topics.sort(key=lambda topic: topic.id)

    legend = ', '.join(topic.mapping() for topic in topics)

    return legend


def return_json(reflections):
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

    available_colors = ['rgba(255, 99, 132, 0.5)', 'rgba(54, 162, 235, 0.5)', 'rgba(255, 206, 86, 0.5)',
                                  'rgba(75, 192, 192, 0.5)', 'rgba(153, 102, 255, 0.5)', 'rgba(255, 159, 64, 0.5)']
    available_border_colors = ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)',
                                  'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)', 'rgba(255, 159, 64, 1)']
    labels = []
    values = []
    background_colors = []
    border_colors = []

    for key in sorted(reflection_dict):
        labels.append(key)
        values.append(reflection_dict[key])
        if key == 'Irrelevant':
            background_colors.append('rgb(150, 150, 150, 0.2)')
            border_colors.append('rgb(150, 150, 150, 0.2')
        else:
            bg_color = available_colors.pop()
            br_color = available_border_colors.pop()
            background_colors.append(bg_color)
            border_colors.append(br_color)

    json = {}
    json['labels'] = labels
    dataset = {}
    dataset['label'] = '% accuracy'
    dataset['data'] = values
    dataset['backgroundColor'] = background_colors
    dataset['borderColor'] = border_colors
    dataset['borderWidth'] = 1
    json['datasets'] = [dataset]
    return json