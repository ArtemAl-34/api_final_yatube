from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import CommentViewSet, GroupViewSet, PostViewSet, FollowViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'follow', FollowViewSet)
router.register(r'posts/(?P<post_id>[^/.]+)/comments',
                CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Получение токена
    path('v1/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена
    path('v1/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Проверка токена
]