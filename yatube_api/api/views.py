from rest_framework import permissions, viewsets

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


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с постами."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]
    pagination_class = PostPagination

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Переопределяет метод создания поста."""
        serializer.save(author=self.request.user)


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

    def get_permissions(self):
        """Устанавливает разрешения для методов."""
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return super().get_permissions()


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
