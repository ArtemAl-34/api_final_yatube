from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, GroupViewSet, PostViewSet, FollowViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'follow', FollowViewSet)
router.register(r'posts/(?P<post_id>[^/.]+)/comments',
                CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', obtain_auth_token, name='api-token-auth'),
]