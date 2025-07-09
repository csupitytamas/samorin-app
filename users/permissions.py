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


class IsAdminAndNotTargetAdmin(BasePermission):
    """
    Csak admin szerkeszthet, admin role-t nem lehet módosítani!
    """

    def has_permission(self, request, view):
        # Csak bejelentkezett admin
        return request.user.is_authenticated and request.user.userprofile.role == 'admin'

    def has_object_permission(self, request, view, obj):
        # Csak ha NEM admin az, akinek módosítaná a szerepét
        return obj.role != 'admin'