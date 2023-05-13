from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import (
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
    ReviewViewSet,
    CommentViewSet,
    UsersViewSet,
    CustomTokenObtainView,
    SignUpView
)


routerv1 = DefaultRouter()

routerv1.register(r"titles", TitleViewSet, basename="titles")
routerv1.register(r"genres", GenreViewSet, basename="genres")
routerv1.register(r"categories", CategoryViewSet, basename="categories")
routerv1.register(r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews")
routerv1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments", CommentViewSet, basename="comments"
)
routerv1.register(r"users", UsersViewSet, basename="users")
# routerv1.register(
#     r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comments"
# )

urlpatterns = [
    path("v1/", include(routerv1.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path(
        'v1/auth/token/',
        CustomTokenObtainView.as_view(),
        name='token_obtain_pair'
    ),
#    path(
#        'v1/auth/token/refresh/',
#        TokenRefreshView.as_view(),
#        name="token_refresh"
#    ),
]
