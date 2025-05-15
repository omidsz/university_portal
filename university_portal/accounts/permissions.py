from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.userrole.role == 'moderator'


class IsMember(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.userrole.role == 'member'


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.userrole.role == 'user'

