from rest_framework import permissions


class IsAuthenticatedOrAuthor(permissions.BasePermission):
    """
    Разрешение, которое позволяет всем пользователям
    выполнять безопасные методы
    и редактировать или удалять объект только его автору.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS)


class IsAuthenticatedForSafeMethods(permissions.BasePermission):
    """
    Разрешение, которое позволяет доступ
    только аутентифицированным пользователям
    для GET и POST запросов.
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST']:
            return request.user.is_authenticated
        return False
