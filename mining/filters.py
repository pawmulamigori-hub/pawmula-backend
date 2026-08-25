import django_filters
from mining.models import MiningStage, MinerProfile


class MiningStageFilter(django_filters.FilterSet):
    published = django_filters.BooleanFilter(field_name="published")

    class Meta:
        model = MiningStage
        fields = ["published"]


class MinerProfileFilter(django_filters.FilterSet):
    published = django_filters.BooleanFilter(field_name="published")
    featured = django_filters.BooleanFilter(field_name="featured")

    class Meta:
        model = MinerProfile
        fields = ["published", "featured"]
