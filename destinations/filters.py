import django_filters
from django.db.models import Q
from destinations.models import Destination


class DestinationFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")
    published = django_filters.BooleanFilter(field_name="published")

    class Meta:
        model = Destination
        fields = ["published", "county"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(location__icontains=value) | Q(county__icontains=value))
