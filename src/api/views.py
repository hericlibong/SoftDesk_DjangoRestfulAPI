from rest_framework.viewsets import ModelViewSet
from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer
# from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     if not self.request.user.is_authenticated:
    #         raise PermissionError("You must be authenticated to create a project.")
    #     serializer.save(author=self.request.user)

    def perform_create(self, serializer):
        # Assigner un auteur par défaut pour les tests sans authentification
        # Utiliser le premier utilisateur comme auteur par défaut
        default_author = get_user_model().objects.first() 
        serializer.save(author=default_author)

class ContributorViewSet(ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

