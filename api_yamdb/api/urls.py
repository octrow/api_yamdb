from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from api.views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

routerv1 = DefaultRouter()

# routerv1.register(r"posts", PostViewSet, basename="posts")
# routerv1.register(r"groups", GroupViewSet, basename="groups")
# routerv1.register(r"follow", FollowViewSet, basename="follow")
# routerv1.register(
#     r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comments"
# )

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("v1/", include(routerv1.urls)),
]

