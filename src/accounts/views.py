from .models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
from .permissions import IsSelfOrAdmin
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    ViewSet pour gérer les opérations CRUD sur le modèle User.
    """
    # queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Limite la liste des utilisateurs en fonction du statut de l'utilisateur authentifié.
        - Les administrateurs voient tous les utilisateurs.
        - Les utilisateurs non administrateurs ne voient que leur propre compte.
        """
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            if self.action == 'list':
                return User.objects.filter(id=self.request.user.id)
            else:
                return User.objects.all()

    def get_permissions(self):
        """
        Attribue les permissions en fonction de l'action.
        - Pour l'action 'create', tout le monde peut créer un compte (AllowAny).
        - Pour l'action 'list', seul un administrateur peut voir tous les utilisateurs.
        - Pour les autres actions, l'utilisateur doit être authentifié et avoir les permissions appropriées.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsSelfOrAdmin]
        return [permission() for permission in permission_classes]