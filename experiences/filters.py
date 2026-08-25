import django_filters
from django.db.models import Q
from experiences.models import Experience


class ExperienceFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")
    published = django_filters.BooleanFilter(field_name="published")
    category = django_filters.CharFilter(field_name="category")

    class Meta:
        model = Experience
        fields = ["published", "category"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))
