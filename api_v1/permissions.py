from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
        )


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return (
            not request.user.is_anonymous
            and request.user.is_moderator
        )

    def has_object_permission(self, request, view, obj):
        return (
            not request.user.is_anonymous
            and request.user.is_moderator
            and request.method == 'DELETE'
        )


class IsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            not request.user.is_anonymous
            and request.user.is_admin
        )

    def has_permission(self, request, view):
        return (
            not request.user.is_anonymous
            and request.user.is_admin
        )
