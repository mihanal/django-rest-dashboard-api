from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_admin:
            return True
        return False


class IsCoach(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_coach:
            return True
        return False


class IsPlayer(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_player:
            return True
        return False

