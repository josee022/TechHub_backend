from rest_framework import permissions # importar la clase permissions de rest_framework

class IsOwnerOrAdmin(permissions.BasePermission):
    """Permite acceso solo al dueño del perfil o a un administrador."""
    def has_object_permission(self, request, view, obj):
        # Los admins pueden hacer cualquier cosa
        if request.user.role == 'admin':
            return True

        # El usuario solo puede modificar su propio perfil
        return obj.user == request.user
