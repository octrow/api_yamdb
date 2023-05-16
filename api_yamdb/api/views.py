from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.filters import TitleFilter
from api.permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrReadOnly,
    IsAdmin,
)
from api.serializer import (
    CategorySerializer,
    CommentSerializer,
    CustomTokenSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleAddSerializer,
    TitleShowSerializer,
    UserEditSerializer,
    UserSerializer,
)
from reviews.models import Category, Genre, Review, Title
from users.models import User

from api.viewset import ListCreateDelMixin


class CategoryViewSet(ListCreateDelMixin):
    """Вьюсет для категорий"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDelMixin):
    """Вьюсет для жанров"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений"""

    queryset = (
        Title.objects.select_related("category")
        .prefetch_related("genre")
        .annotate(rating=Avg("reviews__score"))  # Супер
    )
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    filterset_fields = (
        "name",
        "year",
        "category",
        "genre",
    )
    # ГОТОВО! 1. Нужно добавить бек сортировки.
    # ГОТОВО? 2. а так же бек фильтрации
    # (хотя она есть в settings, но это список, у он переопределяется), и ограничить её в теле Viewset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleShowSerializer
        return TitleAddSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов"""

    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(
            Title, pk=self.kwargs.get("title_id")
        )  # Отлично

    def get_queryset(self):
        # ГОТОВО! Лишняя переменная, потому что одноразовая, можно сразу возвращать(печатать) результат.
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев"""

    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get("review_id"))

    def get_queryset(self):
        # ГОТОВО! Лишняя переменная, потому что одноразовая, можно сразу возвращать(печатать) результат.
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class SignUpView(generics.GenericAPIView):
    """Регистрация новых пользователя по email."""

    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        username_exists = User.objects.filter(
            # Сейчас нет возможности получить новый пин-код, если вдруг потерян первый.
            # Есть 2 решения:
            # 1. Создавать пользователя методом get_or_create, нужно в блоке try
            # с выбросом исключения если будет неверное имя пользователя или емаил (нужно найти верное исключение).
            # 2. Создаем так же как в строках ![serializer = SignUpSerializer...serializer.save]!,
            # но с валидацией в сериализаторе,
            # в нём нужно проверить, что емаил или ник не используется, а так же придется написать метод create.
            username=request.data.get("username"),
            email=request.data.get("email"),
        ).exists()
        if username_exists:
            return Response(request.data, status=status.HTTP_200_OK)
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Отлично
        serializer.save(is_active=False)
        user = User.objects.get(username=serializer.data["username"])
        # Используем шоткат get_object_or_404.
        # Использовать только валидированные данные.
        confirmation_code = default_token_generator.make_token(user)
        user.save()
        email_subject = "Регистрация на сайте"  # Литералы в 137-138 убрать в файл с константами.
        email_message = f"Ваш код подтверждения: {confirmation_code}"
        send_mail(
            email_subject,
            email_message,
            from_email=None,  # А тут должен быть емаил админа и он должен храниться в settings.
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
        user = get_object_or_404(
            User, username=serializer.data["username"]
        )  # Использовать только валидированные данные.

        if (
            user.confirmation_code != confirmation_code
        ):  # Это не работает, вы не проверяли проект перед отправкой?
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
            serializer = UserSerializer(user)

        serializer = UserEditSerializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
