from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = "Вы не являетесь администратором."

    def has_permission(self, request, view):
        return request.user.is_staff


class IsOwner(BasePermission):
    message = "Вы не являетесь владельцем."

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
