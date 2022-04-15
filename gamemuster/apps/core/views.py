from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View


class IndexListView(View):
    template_name = 'index.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('games'))
        return render(self.request, self.template_name)
