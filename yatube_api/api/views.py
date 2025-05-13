from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsAuthor
from .serializers import CommentSerializer, GroupSerializer, PostSerializer, FollowSerializer
from posts.models import Comment, Group, Post, Follow


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с группами."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с постами."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

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


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Возвращает все подписки текущего пользователя."""
        user = self.request.user
        return Follow.objects.filter(user=user)

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

