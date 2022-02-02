from django_filters import FilterSet
from django_filters.filters import CharFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    name = CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    genre = CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )
    category = CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category', )
