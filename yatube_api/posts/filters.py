from django_filters import rest_framework as filters
from .models import Follow  # Импортируйте вашу модель


class FollowFilter(filters.FilterSet):
    class Meta:
        model = Follow
        fields = {
            'user': ['exact'],  # Фильтрация по пользователю
            'following': ['exact'],  # Фильтрация по подпискам
        }
