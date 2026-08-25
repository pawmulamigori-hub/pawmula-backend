import django_filters
from django.db.models import Q
from gallery.models import GalleryItem


class GalleryItemFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")
    category = django_filters.CharFilter(field_name="category")
    fileType = django_filters.CharFilter(field_name="file_type")

    class Meta:
        model = GalleryItem
        fields = ["category"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(caption__icontains=value))
