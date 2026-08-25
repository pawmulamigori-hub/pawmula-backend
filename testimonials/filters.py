import django_filters
from django.db.models import Q
from testimonials.models import Testimonial


class TestimonialFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")
    published = django_filters.BooleanFilter(field_name="published")
    featured = django_filters.BooleanFilter(field_name="featured")

    class Meta:
        model = Testimonial
        fields = ["published", "featured"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(quote__icontains=value))
