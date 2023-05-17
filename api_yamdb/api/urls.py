from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

from api.views import (CategoryViewSet, CommentViewSet, APIGetToken,
                       GenreViewSet, ReviewViewSet, APISignup, TitleViewSet,
                       UsersViewSet)


routerv1 = DefaultRouter()

routerv1.register(r"titles", TitleViewSet, basename="titles")
routerv1.register(r"genres", GenreViewSet, basename="genres")
routerv1.register(r"categories", CategoryViewSet, basename="categories")
routerv1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
routerv1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
routerv1.register(r"users", UsersViewSet, basename="users")


urlpatterns_auth = [
    path('signup/', APISignup.as_view(), name='signup'),
    path('token/', APIGetToken.as_view(),
         name='get_token'),
]

urlpatterns = [
    path('v1/', include(routerv1.urls)),
    path('v1/auth/', include(urlpatterns_auth)),
]
