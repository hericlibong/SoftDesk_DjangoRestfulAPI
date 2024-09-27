from rest_framework.permissions import BasePermission


class IsSelOrAdmin(BasePermission):
    """
    Permisssion qui permet à un utilisateur de modifier ou de supprimer son compte
    ou à un administrateur d'y accéder
    """
    def has_object_permission(self, request, view, obj):
        # Si l'utilisateur est un administrateur, il peut accéder à tous les comptes
        if request.user.is_staff:
            return True
        # sinon il ne peut accéder qu'à ses propres informations
        return obj == request.user