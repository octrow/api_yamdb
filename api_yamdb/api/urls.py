from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import TitleViewSet, GenreViewSet, CategoryViewSet, UsersViewSet

routerv1 = DefaultRouter()

routerv1.register(r"users", UsersViewSet, basename='users')
routerv1.register(r"titles", TitleViewSet, basename="titles")
routerv1.register(r"genres", GenreViewSet, basename="genres")
routerv1.register(r"categorys", CategoryViewSet, basename="categorys")
# routerv1.register(
#     r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comments"
# )

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("v1/", include(routerv1.urls)),
]

