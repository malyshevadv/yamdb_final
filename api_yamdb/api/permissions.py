from rest_framework import permissions

from users.models import User


class IsAuthenticated(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated


class ReadOnly(permissions.BasePermission):
    """Разрешает доступ к безопасным методам."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class IsAuthor(permissions.BasePermission):
    """Разрешает доступ автору."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class IsAdmin(permissions.BasePermission):
    """Разрешает доступ администратору."""

    message = 'Доступ только для администрации.'

    def has_permission(self, request, view):
        return bool(
            request.user.role == User.ADMIN
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.role == User.ADMIN
            or request.user.is_superuser
        )


class IsModerator(permissions.BasePermission):
    """Разрешает доступ модератору."""

    def has_object_permission(self, request, view, obj):
        return request.user.role == User.MODERATOR
