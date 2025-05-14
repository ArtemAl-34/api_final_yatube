from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.pagination import PageNumberPagination
from .permissions import IsAuthor
from .serializers import CommentSerializer, GroupSerializer, PostSerializer, FollowSerializer
from posts.models import Comment, Group, Post, Follow

class PostPagination(PageNumberPagination):
    """Класс пагинации для публикаций."""
    page_size = 10  # Количество публикаций на страницу по умолчанию
    page_size_query_param = 'limit'  # Параметр для указания количества публикаций на страницу
    max_page_size = 100  # Максимальное количество публикаций на страницу

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с группами."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Возвращает все группы, доступные текущему пользователю."""
        # Здесь вы можете добавить дополнительную фильтрацию, если это необходимо
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

    def list(self, request, *args, **kwargs):
        """Получение списка всех публикаций."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)  # Возвращаем только данные постов

    def retrieve(self, request, *args, **kwargs):
        """Получение публикации по id."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Обновление публикации по id."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление публикации по id."""
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Удаление публикации по id."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)

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
        post_id = self.kwargs['post_id']
        comment = self.get_object()
        serializer = self.get_serializer(comment)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Обновление комментария по id."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()  # Получаем экземпляр комментария
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)  # Здесь не передаем post_id
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление комментария по id."""
        # Получаем объект, который нужно обновить
        partial = True  # Указываем, что это частичное обновление
        instance = self.get_object()  # Получаем экземпляр объекта по ID из kwargs

        # Обновляем объект с помощью perform_update
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

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
    
class TokenVerifyView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
            # Логика верификации токена...
        return Response({'valid': True})

