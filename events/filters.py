import django_filters
from events.models import Event


class EventFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")
    status = django_filters.CharFilter(field_name="status")

    class Meta:
        model = Event
        fields = ["status"]

    def filter_search(self, queryset, name, value):
        from django.db.models import Q
        return queryset.filter(Q(name__icontains=value) | Q(location__icontains=value))
