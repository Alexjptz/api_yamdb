from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or
                request.user == obj.author or
                request.user.role in ['admin', 'moderator'])


class IsUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == User.Role.USER


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Role.MODERATOR

    def has_object_permission(self, request, view, obj):
        return request.user.role == User.Role.MODERATOR


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Role.ADMIN or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.role == User.Role.ADMIN or request.user.is_superuser


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                request.user.role == User.Role.ADMIN)
