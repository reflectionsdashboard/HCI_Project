from django.shortcuts import render, HttpResponse
from reflections.models import *


def show_expert_view(request):
    reflections = Reflection.objects.all()
    paired_reflections = [reflections[n:n+2] for n in range(0, len(reflections), 2)]
    topics = Topic.objects.all()
    inaccuracy_categories = InAccuracyCategory.objects.all()

    return render(request, 'expert/expert_page.html', {'reflections': paired_reflections, 'topics': topics,
                                                       'inaccuracy_categories': inaccuracy_categories})


def submit_analysis(request):

    print("Submitting Data")
    return HttpResponse("Submitting Data")
