from django.shortcuts import render, HttpResponse
from reflections.models import Reflection
from reflections.forms import ReflectionForm
from django.forms import modelformset_factory
from expert.twitter import TwitterAPI
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required(login_url="/accounts/signin")
def show_expert_view(request):
    TwitterAPI.get_tweets()

    reflection_form_set = modelformset_factory(Reflection, form=ReflectionForm, exclude=(), extra=0)
    form_set = reflection_form_set(queryset=Reflection.objects.filter(is_pending=True))
    # form_set = form_chunks(form_set.forms, 2)
    return render(request, 'expert/expert_page.html', {'reflection_form_set': form_set})


def submit_analysis(request):
    reflection_form_set = modelformset_factory(Reflection, form=ReflectionForm, exclude=(), extra=0)
    formset = reflection_form_set(request.POST, queryset=Reflection.objects.filter(is_pending=True))

    for reflection_form in formset:
        if reflection_form.is_valid() and reflection_form.has_changed():
            reflection = reflection_form.save(commit=False)
            if 'description' in reflection_form.changed_data:
                reflection_form.changed_data.remove('description')

            if len(reflection_form.changed_data) > 0:
                    print("---------PRINT----------")
                    print(reflection_form.changed_data)
                    print(reflection)

                    reflection.is_pending = False
                    reflection_form.save()

    return show_expert_view(request)

def form_chunks(forms, size):
    return [forms[i:i + size] for i in range(0, len(forms), size)]





