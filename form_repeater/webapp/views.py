from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from .models import *
from .forms import *


class Home(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'home.html'
    success_url = reverse_lazy('thanks')

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        if self.request.POST:
            context["category_formset"] = inspection_form_category(self.request.POST or None,
                                                                              self.request.FILES or None,
                                                                              prefix='category')
        else:
            context["category_formset"] = inspection_form_category(prefix='category')

        if self.request.POST:
            context["question_formset"] = category_question(self.request.POST or None,
                                                                              self.request.FILES or None,
                                                                              prefix='question')
        else:
            context["question_formset"] = category_question(prefix='question')

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        category_formset = context["category_formset"]
        question_formset = context["question_formset"]
        if category_formset.is_valid():

            self.object = form.save()

            category_formset.instance = self.object
            category_instance = category_formset.save()

            question_formset.instance = category_instance
            question_formset.save()

            return super(Home, self).form_valid(form)
        else:
            print(category_formset.errors)
            print(question_formset.errors)
            return super(Home,self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(Home, self).get_form_kwargs()
        kwargs['use_required_attribute'] = False
        return kwargs


class ThanksTemplate(TemplateView):
    template_name = 'thanks.html'


def home(request):

    if request.method == "POST":
        form = SubjectForm(request.POST)
        category_formset = inspection_form_category(request.POST, prefix='category')
        if form.is_valid() and category_formset.is_valid():
            subject = form.save(commit=False)
            subject.save()

            category = category_formset.save(commit=False)
            category.subject = subject
            category.save()

            return redirect('thanks')
    else:
        form = SubjectForm()
        category_formset = inspection_form_category(prefix='category')

    context = {
        'form':form,
        'category_formset':category_formset,
    }
    return render(request, 'home.html', context)