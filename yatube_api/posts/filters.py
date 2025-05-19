from django_filters import rest_framework as filters
from .models import Follow


class FollowFilter(filters.FilterSet):
    class Meta:
        model = Follow
        fields = {
            'user': ['exact'],
            'following': ['exact'],
        }
