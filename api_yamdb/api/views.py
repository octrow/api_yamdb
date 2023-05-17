from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework.decorators import action, api_view, permission_classes

from api_yamdb.settings import DEFAULT_FROM_EMAIL
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
    GetTokenSerializer,
)
from reviews.models import Category, Genre, Review, Title
from users.models import User

from api.viewset import ListCreateDelMixin


EMAIL_SUBJECT = 'Регистрация на сайте'
CORRECT_CODE_EMAIL_MESSAGE = 'Код подтверждения: {code}.'
USERNAME_EMAIL_ALREADY_EXISTS = 'Такое username или email уже занято.'
INVALID_CODE = 'Неверный код подтверждения.'


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
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    # Нужно добавить бек сортировки, а так же бек фильтрации
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
        title = get_object_or_404(
            Title, pk=self.kwargs.get("title_id")
        )  # Лишняя переменная, потому что одноразовая, можно сразу возвращать(печатать) результат.
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев"""

    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get("review_id"))

    def get_queryset(self):
        review = (
            self.get_review()
        )  # Лишняя переменная, потому что одноразовая, можно сразу возвращать(печатать) результат.
        return review.comments.all()

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
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)

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
        username = serializer.data.get('username')
        email = serializer.data.get('email')
        user, created = User.objects.get_or_create(
            username=username,
            email=email
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
        subject='Код подтверждения.',
        message=f'Здравствуйте, {user.username}.'
                f'\nКод подтверждения для доступа: {confirmation_code}',
        from_email=DEFAULT_FROM_EMAIL,
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

        serializer = UserEditSerializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)