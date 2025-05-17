from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Post, Group, Follow, User

class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""
    class Meta:
        model = Group
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ['author', 'post']

class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(slug_field='username',
                                             queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ['user', 'following']
        read_only_fields = ['user']

    def validate_following(self, value):
        """Проверка, что пользователь не может подписаться на самого себя."""
        request = self.context.get('request')
        if value == request.user:
            raise serializers.ValidationError("Вы не можете подписаться на самого себя.")
        return value

    def validate(self, attrs):
        """Проверка уникальности подписки."""
        user = self.context['request'].user
        following = attrs.get('following')
        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError("Вы уже подписаны на этого пользователя.")
        return attrs

    def create(self, validated_data):
        """Создание новой подписки."""
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)