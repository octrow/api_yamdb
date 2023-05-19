from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.mixins import ListCreateDelMixin
from api.permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.serializer import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleAddSerializer,
    TitleShowSerializer,
    UserEditSerializer,
    UserSerializer,
)
from api_yamdb import constances

# ГОТОВО! Как достать
# правильно файл настроек клик
# https://docs.djangoproject.com/en/4.0/topics/settings/#using-settings-in-
# python-code
from reviews.models import Category, Genre, Review, Title
from users.models import User

# ГОТОВО! Константу убираем в файл с константами.


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
        .annotate(rating=Avg("reviews__score"))
    )
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    # ГОТОВО! Бек для фильтрации вижу, а вот
    # бека для сортировки нет. Так же не вижу ограничения по каким полям
    # сортировка разрешена. Ссылка есть в прошлом ревью.
    # old: Нужно добавить бек сортировки, а так же бек фильтрации (хотя она
    # есть в settings, но это список, у он переопределяется), и ограничить её
    # в теле Viewset https://www.django-rest-framework.org/api-guide/filtering/
    # #specifying-which-fields-may-be-ordered-against
    ordering_fields = ("rating", "name", "year")
    filterset_class = TitleFilter
    filterset_fields = (
        "name",
        "year",
        "category",
        "genre",
    )

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleShowSerializer
        return TitleAddSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов"""

    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
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
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class APIGetToken(APIView):
    """
    Получение JWT-токена в обмен на username и confirmation code.
    Пример тела запроса:
    {
        "username": "string",
        "confirmation_code": "string"
    }
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data["username"])
        # try:  # ГОТОВО! Вместо блока try и get нужен get_object_or_404
        #     user = User.objects.get(username=data["username"])
        # except User.DoesNotExist:
        #     return Response(
        #         {"username": "Пользователь не найден!"},
        #         status=status.HTTP_404_NOT_FOUND,
        #     )
        if default_token_generator.check_token(
            user, data.get("confirmation_code")
        ):
            # (data.get("confirmation_code") == user.confirmation_code):
            # ГОТОВО! Это не то,
            # если мы используем default_token_generator для генерации
            # пин-кода, то нужно использовать его и для проверки пин-кода.
            token = RefreshToken.for_user(user).access_token
            return Response(
                {"token": str(token)}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"confirmation_code": "Неверный код подтверждения!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class APISignup(APIView):
    """
    Получить код подтверждения на переданный email.
    Пример тела запроса:
    {
        "email": "string",
        "username": "string"
    }.
    """

    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get("username")
        email = serializer.data.get("email")
        try:
            user, _ = User.objects.get_or_create(
                username=username, email=email
            )
        except IntegrityError:
            error_message = (
                constances.EMAIL_TAKEN_ERROR
                if User.objects.filter(email=email).exists()
                else constances.USERNAME_TAKEN_ERROR
            )
            return Response(
                error_message,
                status=status.HTTP_400_BAD_REQUEST,
            )
            # return Response(
            # ГОТОВО!"Ошибка при попытке создать новую запись",  # Лучше выдать
            #     # конкретную ошибку для каждого поля, можно сделать так:
            #     # - создать 2 текстовые константы для разных ошибок, например
            #     # Электронная почта уже занята!
            #     # - записать в тернарник так: переменная = ПЕРВАЯ_КОНСТАНТА
            #     # если Юсер.отфильтрован(емаил=емаил).существует()
            #     # иначе ВТОРАЯ_КОНСТАНТА
            #     status=status.HTTP_400_BAD_REQUEST,
            # )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            constances.SUBJECT,
            message=constances.MESSAGE_EMAIL.format(
                user.username, confirmation_code
            ),
            # ВОЗМОЖНО ГОТОВО?!
            # message=f"Здравствуйте, {user.username}."  # Текстовые константы
            # # выносим в файл для констант. Наполнять их можно через формат.
            # f"\nКод подтверждения для доступа: {confirmation_code}",
            from_email=constances.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


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
            # ВОЗМОЖНО ГОТОВО? А вот условие зря убрали получается если метод patch то
            # выполниться и 197 строка и 199, зачем нам это?

        if request.method == "PATCH":
            serializer = UserEditSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
