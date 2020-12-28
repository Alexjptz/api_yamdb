from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class IsOwnerOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or
                request.user == obj.author or
                request.user.is_superuser)


class IsModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.role == User.Role.MODERATOR)
