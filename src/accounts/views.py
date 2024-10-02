from .models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsSelfOrAdmin
from .serializers import UserSerializer
from api.models import Project, Issue, Comment


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsSelfOrAdmin]
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()

        # Vérification des permissions
        if not (request.user.is_staff or request.user == user):
            raise PermissionDenied("Vous n'êtes pas autorisé à supprimer cet utilisateur.")

        Project.objects.filter(author=user).delete()
        Issue.objects.filter(author=user).delete()
        Comment.objects.filter(author=user).delete()

        user.delete()

        return Response({"message": "Les données de l'utilisateur ont été supprimées avec succès."},
                        status=status.HTTP_204_NO_CONTENT)

    def destroy_self(self, request, *args, **kwargs):
        """
        Permet à l'utilisateur de supprimer son propre compte.
        """
        # Récupérer l'utilisateur actuel via request.user
        user = request.user

        Project.objects.filter(author=user).delete()
        Issue.objects.filter(author=user).delete()
        Comment.objects.filter(author=user).delete()

        user.delete()

        return Response({"message": "Votre compte a été supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
