from rest_framework.permissions import BasePermission,SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Faqat adminuserlargagina ruxsat beruvchi permission class.
    Qolgan barcha foydalanuvchilarga faqat o'qishgagina huquq beriladi."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff
