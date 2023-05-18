from rest_framework import filters, mixins, viewsets

from api.permissions import IsAdminOrReadOnly


class ListCreateDelMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Миксин для вьюсетов"""

    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("=name",)
