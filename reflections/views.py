from django.shortcuts import render,redirect
from reflections.models import *
from django.http import HttpResponseRedirect
from .forms import SubTopicForm

import json


# Create your views here.

# def show_reflections_view(request):

#     reflection_form_set = modelformset_factory(Reflection, form=ReflectionForm, exclude=(), extra=0)
#     form_set = reflection_form_set(queryset=Reflection.objects.filter(is_pending=True))
#     # form_set = form_chunks(form_set.forms, 2)
#     return render(request, 'reflections/reflections.html', {'reflection_form_set': form_set})




subject_topics = {}

def show_reflections_view(request):

	if request.method == 'POST':
		form = SubTopicForm(request.POST)
		if form.is_valid():
			
			chosenSubject = form.cleaned_data["subject"];
			chosenTopic = form.cleaned_data["topic"]
			# print(chosenSubject);
			if chosenTopic == "NULL":
				sub = Subject.objects.get(name=chosenSubject);
				reflections = Reflection.objects.filter(is_pending=False, subject=sub).order_by('date')[:5][::-1]
			else:
				sub = Subject.objects.get(name=chosenSubject);
				top = Topic.objects.get(name=chosenTopic);
				reflections = Reflection.objects.filter(is_pending=False, subject=sub, topic=top).order_by('date')[:5][::-1]
			
			subject_topics = return_subject_topic(Reflection.objects.filter(is_pending=False).order_by('date')[:5][::-1])

			subjects = []
			topics = []

			for subject in subject_topics:
				sub = {"name":subject};
				subjects.append(sub);
				if subject == chosenSubject:
					for topic in subject_topics[subject]:
						top = {"name":topic};
						topics.append(top);

			return render(request, "reflections/reflections.html", {"reflections": reflections, "subjects": subjects, "topics":topics,
    			"Subject": chosenSubject, "Topic":chosenTopic})
	

	chosenSubject = "NULL"
	chosenTopic = "NULL"

	reflections = Reflection.objects.filter(is_pending=False).order_by('date')[:5][::-1]
	subject_topics = return_subject_topic(reflections)
	subjects = []
	topics = []

	for subject in subject_topics:
		sub = {"name":subject};
		subjects.append(sub);

	return render(request, "reflections/reflections.html", {"reflections": reflections, "subjects": subjects, "topics":topics,
    	"Subject": chosenSubject, "Topic":chosenTopic})

def return_subject_topic(reflections):
	SubTop = {};
	for reflection in reflections:
		if reflection.topic is None or reflection.subject is None:
			continue;
		if str(reflection.subject) not in SubTop:
			SubTop[str(reflection.subject)] = [];
		if str(reflection.topic) not in SubTop[str(reflection.subject)]:
			SubTop[str(reflection.subject)].append(str(reflection.topic));
	# for subject in SubTop:
		# 
	return SubTop;

def reflections_filter(request):
	pass