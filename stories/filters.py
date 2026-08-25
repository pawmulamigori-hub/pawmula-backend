import django_filters
from django.db.models import Q
from stories.models import Story


class StoryFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")
    published = django_filters.BooleanFilter(field_name="published")
    featured = django_filters.BooleanFilter(field_name="featured")
    category = django_filters.CharFilter(field_name="category")
    status = django_filters.CharFilter(field_name="status")

    class Meta:
        model = Story
        fields = ["published", "featured", "category", "status"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(excerpt__icontains=value) | Q(author__icontains=value))
