from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import *


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


class BaseCategoryFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(BaseCategoryFormset, self).add_fields(form, index)

        form.nested = category_question(
                                instance=form.instance,
                                data=form.data if form.is_bound else None,
                                prefix='question-%s-%s' % (
                                    form.prefix,
                                    category_question.get_default_prefix()),
                                )

    def is_valid(self):
        result = super(BaseCategoryFormset, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()
                form.empty_permitted = False

        return result

    def save(self, commit=True):
        result = super(BaseCategoryFormset, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result


inspection_form_category = inlineformset_factory(Subject, Category, form=CategoryForm, extra=3,
                                                 validate_max=True, validate_min=True)
category_question = inlineformset_factory(Category, Question, QuestionForm, extra=1)
