from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    Viewset pour gérer les opérations CRUD sur le modèle User.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Limite la liste des utilisateurs en fonction du statut de l'utilisateur authentifié.
        - les administrateurs peuvent voir tous les utilisateurs
        - Les utilisateurs non administrateurs ne peuvent voir que leur propre compte
        """
        if self.request.user.is_staff:
            return User.objects.all()  # Les admins peuvent voir tous les utilisateurs
        return User.objects.filter(id=self.request.user.id) # Les utilisateurs normaux ne peuvent voir que leur propre compte

    def get_permissions(self):
        """ 
        Attribue les permissions en fonction de l'action effectuée.
        - Pour l'action 'create', tout le monde peut créer un compte (AllowAny).
        - Pour les autres actions, l'utilisateur doit être authentifié (IsAuthenticated).
        """
        if self.action == 'create':
            permission_classes = [AllowAny]  # Permettre à tout le monde de s'inscrire/créer un compte
        else:
            permission_classes = [IsAuthenticated] # Les autres 
        # Retourne les permissions appropriées en fonction de l'action
        return [permission() for permission in permission_classes]
    
    # def destroy(self, request, *args, **kwargs):
    #     """
    #     Supprime un utilisateur et renvoie un message de confirmation.
    #     """
    #     # écrire un message quand un utilisateur est supprimé
    #     user = self.get_object()
    #     user.delete()
    #     return Response({"message": "L'utilisateur a été supprimé avec succès"}, status=status.HTTP_200_OK)
      
    # Surcharger la méthode retrieve pour s'assurer que 
    # les utilisateurs ne peuvent récuperer que leurs propres informations
    def retrieve(self, request, *args, **kwargs):
        """
        Récupère les informations d'un utilisateur spécifique.
        - Les administrateurs peuvent voir tous les utilisateurs
        - Les utilisateurs non administrateurs ne peuvent voir que leur propre compte
        """
        if not request.user.is_staff and int(kwargs['pk']) != request.user.id:
            return Response({"message": "Vous n'êtes pas autorisé à accéder à ces informations"}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """
        Met à jour les informations d'un utilisateur.
        - Les administrateurs peuvent mettre à jour tous les utilisateurs
        - Les utilisateurs non administrateurs ne peuvent mettre à jour que leur propre compte
        """
        if not request.user.is_staff and int(kwargs['pk']) != request.user.id:
            return Response({"message": "Vous n'êtes pas autorisé à mettre à jour ces informations"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Met à jour partiellement les informations d'un utilisateur.
        - Les administrateurs peuvent mettre à jour tous les utilisateurs
        - Les utilisateurs non administrateurs ne peuvent mettre à jour que leur propre compte
        """
        if not request.user.is_staff and int(kwargs['pk']) != request.user.id:
            return Response({"message": "Vous n'êtes pas autorisé à mettre à jour ces informations"}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)
    
    def distroy(self, request, *args, **kwargs):
        """
        Supprime un utilisateur.
        - Les administrateurs peuvent supprimer tous les utilisateurs
        - Les utilisateurs non administrateurs ne peuvent supprimer que leur propre compte
        """
        if not request.user.is_staff and int(kwargs['pk']) != request.user.id:
            return Response({"message": "Vous n'êtes pas autorisé à supprimer cet utilisateur"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)