from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin'

class IsCrewOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return hasattr(request.user, 'userprofile') and request.user.userprofile.role in ['crew', 'admin']

class IsChiefOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return hasattr(request.user, 'userprofile') and request.user.userprofile.role in ['chief', 'admin']