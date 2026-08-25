import django_filters
from django.db.models import Q
from bookings.models import Booking


class BookingFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")
    status = django_filters.CharFilter(field_name="status")

    class Meta:
        model = Booking
        fields = ["status"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(customer_name__icontains=value) | Q(reference__icontains=value))
