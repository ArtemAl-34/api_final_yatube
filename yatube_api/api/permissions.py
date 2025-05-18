from rest_framework import permissions


class IsAuthenticatedOrAuthor(permissions.BasePermission):
    """
    Разрешение, которое позволяет редактировать или удалять
     объект только его автору.
    """ 
    def has_permission(self, request, view):
        # Разрешаем безопасные методы для всех
        if request.method in permissions.SAFE_METHODS:
            return True
        # Для всех остальных методов проверяем аутентификацию
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
