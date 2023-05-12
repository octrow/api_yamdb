from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status, filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsAdminOrReadOnly, IsAuthenticatedOrReadOnly

from reviews.models import Genre, Title, Category, Review
from api.serializer import (
    GenreSerializer,
    TitleShowSerializer,
    TitleAddSerializer,
    CategorySerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    UserEditSerializer,
    SignUpSerializer,
    CustomTokenSerializer,
)
from .permissions import IsAdmin
from users.models import User
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для категорий"""

    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CategorySerializer

    def delete(self, request, pk=None):
        instance = self.get_object(pk)
        if request.user.is_admin:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений"""

    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleShowSerializer
        return TitleAddSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для жанров"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get("review_id"))

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


# from django.shortcuts import get_object_or_404
# from rest_framework import filters, viewsets, mixins
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.permissions import IsAuthenticated

# from .permissions import IsOwnerOrReadOnly
# from .serializers import (
#     CommentSerializer,
#     FollowSerializer,
#     GroupSerializer,
#     PostSerializer,
# )
# from posts.models import Group, Post


# class CommentViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentSerializer
#     permission_classes = (IsOwnerOrReadOnly,)

#     def get_post(self):
#         return get_object_or_404(Post, id=self.kwargs.get("post_id"))

#     def get_queryset(self):
#         return self.get_post().comments.all()

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user, post=self.get_post())


# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all().select_related("author")
#     serializer_class = PostSerializer
#     pagination_class = LimitOffsetPagination
#     permission_classes = (IsOwnerOrReadOnly,)

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


# class GroupViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer


# class FollowViewSet(
#     mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
# ):
#     serializer_class = FollowSerializer
#     permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ("following__username",)

#     def get_queryset(self):
#         return self.request.user.follower.all()


class SignUpView(generics.GenericAPIView):
    """Регистрация новых пользователя по email."""

    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        username_exists = User.objects.filter(
            username=request.data.get("username"),
            email=request.data.get("email"),
        ).exists()
        if username_exists:
            return Response(request.data, status=status.HTTP_200_OK)
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_active=False)
        user = User.objects.get(username=serializer.data["username"])
        confirmation_code = default_token_generator.make_token(user)
        user.save()
        email_subject = "Регистрация на сайте"
        email_message = f"Ваш код подтверждения: {confirmation_code}"
        send_mail(
            email_subject,
            email_message,
            from_email=None,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomTokenObtainView(TokenObtainPairView):
    """Выдача токена."""

    permission_classes = (AllowAny,)

    def post(self, request):
        confirmation_code = request.data.get("confirmation_code")
        serializer = CustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.data["username"])
        if user.confirmation_code != confirmation_code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        token = RefreshToken.for_user(user)
        return Response(
            {"token": str(token.access_token)}, status=status.HTTP_200_OK
        )


class UsersViewSet(viewsets.ModelViewSet):

    """Получение списка всех пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, IsAuthenticatedOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    search_fields = ("username",)
    lookup_field = "username"
    http_method_names = ["get", "post", "patch", "delete"]

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        url_path="me",
        permission_classes=(IsAuthenticated,),
    )
    def user_me_profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == "PATCH":
            serializer = UserEditSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
