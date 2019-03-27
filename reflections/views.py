import json
from django.shortcuts import render
from reflections.models import *
from django.http import JsonResponse


def show_reflections_view(request):
	return render(request, 'reflections/reflections.html')


def get_reflection_data(request):
	user_id = request.user
	subject_id = request.GET['subject']
	topic_id = request.GET['topic']

	if subject_id == '0':
		if topic_id == '0':
			reflections = Reflection.objects.filter(student_handle=user_id, is_pending=False).order_by(
				'date')
		else:
			reflections = Reflection.objects.filter(student_handle=user_id, is_pending=False, topic_id=topic_id).order_by('date')
	else:
		if topic_id == '0':
			reflections = Reflection.objects.filter(student_handle=user_id, is_pending=False, subject_id=subject_id).order_by(
				'date')
		else:
			reflections = Reflection.objects.filter(student_handle=user_id, is_pending=False, subject_id=subject_id,
													topic_id=topic_id).order_by('date')

	return render(request, "reflections/data.html", {"reflections": reflections})


def get_subject_data(request):
	subjects = list(Subject.objects.all().order_by('name').values())
	return JsonResponse(subjects, safe=False)


def get_topic_data(request):
	subject_id = request.GET['subject']
	if subject_id == '0':
		topics = list(Topic.objects.all().order_by('subject_id').values())
	else:
		topics = list(Topic.objects.filter(subject_id=subject_id).order_by('name').values())
	return JsonResponse(topics, safe=False)
