from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import TitleViewSet, GenreViewSet, CategoryViewSet

routerv1 = DefaultRouter()

routerv1.register(r"titles", TitleViewSet, basename="titles")
routerv1.register(r"genres", GenreViewSet, basename="genres")
routerv1.register(r"categorys", CategoryViewSet, basename="categorys")
# routerv1.register(
#     r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comments"
# )


urlpatterns = [
    path("v1/", include(routerv1.urls)),
]
