from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from .pagination import PostPagination
from .permissions import IsAuthor
from .serializers import (
    CommentSerializer,
    GroupSerializer,
    PostSerializer,
    FollowSerializer,
)
from posts.models import Comment, Group, Post, Follow


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с группами."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Возвращает все группы, доступные текущему пользователю."""
        return super().get_queryset()

    def retrieve(self, request, *args, **kwargs):
        """Получение информации о сообществе по id."""
        return super().retrieve(request, *args, **kwargs)


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с постами."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]
    pagination_class = PostPagination

    def get_queryset(self):
        return Post.objects.all()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Переопределяет метод создания поста."""
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Получение публикации по id."""
        return self.get_post_response(*args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Обновление публикации по id."""
        return self.update_post_response(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление публикации по id."""
        return self.update_post_response(request, *args,
                                         partial=True, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Удаление публикации по id."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)

    def get_post_response(self, *args, **kwargs):
        """Общий метод для получения поста и его сериализации."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update_post_response(self, request, *args, **kwargs):
        """Общий метод для обновления поста."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]

    def get_queryset(self):
        """Возвращает набор комментариев для конкретного поста."""
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        """Переопределяет метод создания комментария."""
        post_id = self.kwargs['post_id']
        serializer.save(author=self.request.user, post_id=post_id)

    def retrieve(self, request, *args, **kwargs):
        """Получение комментария по id."""
        return self._get_comment_response()

    def update(self, request, *args, **kwargs):
        """Обновление комментария по id."""
        return self._update_comment(request, partial=False)

    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление комментария по id."""
        return self._update_comment(request, partial=True)

    def destroy(self, request, *args, **kwargs):
        """Удаление комментария по id."""
        comment = self.get_object()
        self.perform_destroy(comment)
        return Response(status=204)

    def get_permissions(self):
        """Устанавливает разрешения для методов."""
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def _get_comment_response(self):
        """Общая логика для получения комментария по id."""
        comment = self.get_object()
        serializer = self.get_serializer(comment)
        return Response(serializer.data)

    def _update_comment(self, request, partial):
        """Общая логика для обновления комментария."""
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class FollowViewSet(viewsets.ModelViewSet):
    """ViewSet для управления подписками пользователей."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Возвращает список подписок текущего пользователя."""
        user = self.request.user
        queryset = Follow.objects.filter(user=user)

        search_username = self.request.query_params.get('search', None)
        if search_username:
            queryset = queryset.filter(
                following__username__icontains=search_username
            )

        return queryset

    def create(self, request, *args, **kwargs):
        """Подписка на пользователя."""
        following_id = request.data.get('following')
        if following_id == request.user.id:
            return Response(
                {'error': 'Вы не можете подписаться на самого себя.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
