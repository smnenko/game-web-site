from django.db.models import Exists, Case, Value, When, BooleanField
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from games.models import Musts


class OrderingMixin(MultipleObjectMixin):
    available_orderings = []
    ordering_field = 'ordering'
    ordering_type = 'order'

    def get_ordering(self):
        ordering = self.request.GET.get(self.ordering_field)
        order = self.request.GET.get(self.ordering_type)

        if ordering in self.available_orderings:
            if order == 'asc':
                return ordering
            if order == 'desc':
                return f'-{ordering}'
        return super().get_ordering()


class MustSingleRequiredMixin(SingleObjectMixin):
    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return (
            super().get_queryset()
            .annotate(status=Exists(
                Musts.objects.filter(user=self.request.user, game__id=pk))
            )
        )


class MustMultipleRequiredMixin(MultipleObjectMixin):
    def get_queryset(self):
        musts = []
        if self.request.user.is_authenticated:
            musts = Musts.objects.filter(user=self.request.user).values_list('game_id', flat=True)

        return (
            super()
            .get_queryset()
            .annotate(
                status=Case(When(id__in=musts, then=Value(True)), default=Value(False), output_field=BooleanField())
            )
        )
