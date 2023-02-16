from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('HEAD', 'OPTIONS', 'GET'):
            return True
        return request.user and request.user.is_staff
