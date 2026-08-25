import django_filters
from faqs.models import FAQ


class FAQFilter(django_filters.FilterSet):
    published = django_filters.BooleanFilter(field_name="published")

    class Meta:
        model = FAQ
        fields = ["published"]
