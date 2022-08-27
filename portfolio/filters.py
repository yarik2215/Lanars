from django_filters import rest_framework as filters

from portfolio.models import Image


class NumberInFilter(filters.NumberFilter, filters.BaseInFilter):
    pass


class ImageFilter(filters.FilterSet):
    portfolio = NumberInFilter(field_name="portfolio")
    name = filters.CharFilter(field_name="name", lookup_expr="contains")
    description = filters.CharFilter(field_name="description", lookup_expr="contains")

    class Meta:
        model = Image
        fields = ['portfolio', 'name', 'description']