# accounts/permissions.py

from rest_framework.permissions import BasePermission

class IsAdminUserProfile(BasePermission):
    """
    Permite acceso solo a usuarios con rol de administrador.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role == 'admin'
        )

class IsAdminOrReadOnly(BasePermission):
    """
    Permite acceso completo solo a administradores.
    Los demás usuarios solo tienen acceso de lectura.
    """
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role == 'admin'
        )

class IsAdminOrOwner(BasePermission):
    """
    Permite a administradores hacer todo.
    Permite a usuarios modificar solo su propio perfil.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
            
        # Si el objeto es un UserProfile
        if hasattr(obj, 'user'):
            return (
                request.user.profile.role == 'admin' or
                obj.user == request.user
            )
        # Si el objeto es un User
        return (
            request.user.profile.role == 'admin' or
            obj == request.user
        )

class CanCreateAdmin(BasePermission):
    """
    Permite crear usuarios administradores solo a otros administradores.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        # Verificar si se está intentando crear un administrador
        role = request.data.get('role', 'student')
        if role == 'admin':
            return (
                hasattr(request.user, 'profile') and
                request.user.profile.role == 'admin'
            )
        return True