from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import ProcessFormView

from core.mixins import MultipleFormsMixin


class MultipleFormsView(TemplateResponseMixin, MultipleFormsMixin, ProcessFormView):
    pass


class IndexListView(View):
    template_name = 'core/landing.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('games'))
        return render(self.request, self.template_name)
