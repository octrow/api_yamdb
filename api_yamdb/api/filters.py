from django_filters import CharFilter, ChoiceFilter, FilterSet

from api_yamdb import constances
from reviews.models import Title


class TitleFilter(FilterSet):
    category = CharFilter(field_name="category__slug", lookup_expr="iexact")
    genre = CharFilter(field_name="genre__slug", lookup_expr="iexact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    year = ChoiceFilter(
        field_name="year",
        choices=[
            (y, y) for y in range(constances.MINYEAR, constances.CURRENTYEAR)
        ],
    )

    class Meta:
        model = Title
        fields = "__all__"
