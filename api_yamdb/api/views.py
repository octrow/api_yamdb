from rest_framework import viewsets, status, filters
from reviews.models import Genre, Title, Category
from users.models import User
from django.shortcuts import get_object_or_404
from .permissions import IsAdmin
from api.serializer import (GenreSerializer, TitleSerializer,
                            CategorySerializer, UserSerializer)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


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


class UsersViewSet(viewsets.ModelViewSet):

    """Получение списка всех пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(methods=['get', 'patch'],
        detail=False, url_path='me',
        permission_classes=(IsAuthenticated,),
    )

    def user_get_profile(self, request):
        if request.method == "GET":
            serializer = self.serializer_class(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.serializer_class(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

