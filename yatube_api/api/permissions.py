from rest_framework import permissions

class IsAuthor(permissions.BasePermission):
    """
    Разрешение, которое позволяет редактировать или удалять
     объект только его автору.
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
