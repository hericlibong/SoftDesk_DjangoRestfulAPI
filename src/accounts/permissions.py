from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsSelfOrAdmin(BasePermission):
    """
    Permisssion personnalisée qui permet à un utilisateur de modifier ou de supprimer son compte
    ou à un administrateur d'y accéder
    """

    message = "Vous n'avez pas la permission d'accéder à ces informations."

    def has_object_permission(self, request, view, obj):
        # Si l'utilisateur est un administrateur, il a accès à tous les objets
        if request.user.is_staff:
            return True
        # Sinon, il ne peut accéder qu'à ses propres informations
        if obj == request.user:
            return True
        # Lever une exception avec un message personnalisé
        raise PermissionDenied(self.message)
