from django.shortcuts import render, HttpResponseRedirect
from django.forms import modelformset_factory
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from reflections.models import Reflection
from reflections.forms import ReflectionForm
from expert.twitter import TwitterAPI


@staff_member_required(login_url="/accounts/signin")
def show_expert_view(request):
    query = Reflection.objects.filter(is_pending=True).order_by('date')
    paginator = Paginator(query, 10)  # Show 10 forms per page
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    page_query = query.filter(id__in=[object.id for object in objects])

    reflection_form_set = modelformset_factory(Reflection, form=ReflectionForm, exclude=(), extra=0)

    if request.method == 'POST':
        form_set = reflection_form_set(request.POST, queryset=page_query)
        for reflection_form in form_set:
            if reflection_form.is_valid() and reflection_form.has_changed():
                reflection = reflection_form.save(commit=False)
                if 'description' in reflection_form.changed_data:
                    reflection_form.changed_data.remove('description')

                if len(reflection_form.changed_data) > 0 and reflection.accuracy is not None:
                    print("---------PRINT----------")
                    print(reflection_form.changed_data)
                    print(reflection)

                    reflection.is_pending = False
                    reflection_form.save()
                return HttpResponseRedirect('/expert')
            else:
                context = {'reflections': objects, 'formset': form_set, 'student_name': 'Expert'}
                return render(request, 'expert/expert_page.html', context)
    else:
        # TwitterAPI.get_tweets()
        form_set = reflection_form_set(queryset=page_query)
        context = {'reflections': objects, 'formset': form_set, 'student_name': 'Expert'}
        return render(request, 'expert/expert_page.html', context)





