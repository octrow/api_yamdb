from django_filters import CharFilter, FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    category = CharFilter(field_name="category__slug", lookup_expr="iexact")
    genre = CharFilter(field_name="genre__slug", lookup_expr="iexact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    year = CharFilter(field_name="year", lookup_expr="iexact")

    class Meta:
        model = Title
        fields = "__all__"
