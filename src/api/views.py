from rest_framework.viewsets import ModelViewSet
from .models import Project, Contributor, Issue, Comment
from .serializers import (ProjectSerializer, ContributorSerializer, 
                          CommentSerializer, IssueSerializer)
# from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model



class ProjectViewSet(ModelViewSet):
    # queryset = Project.objects.all()
    queryset = Project.objects.prefetch_related('contributors', 'issues')  # Précharge les relations
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

    def get_queryset(self):
        project_id = self.kwargs['project_pk']
        return Contributor.objects.filter(project__id=project_id)
    

class IssueViewSet(ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        # Assigner un auteur par défaut pour les tests sans authentification
        # Utiliser le premier utilisateur comme auteur par défaut
        default_author = get_user_model().objects.first() 
        serializer.save(author=default_author)

    def get_queryset(self):
        project_id = self.kwargs['project_pk']
        return Issue.objects.filter(project__id=project_id)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        # Assigner un auteur par défaut pour les tests sans authentification
        # Utiliser le premier utilisateur comme auteur par défaut
        default_author = get_user_model().objects.first() 
        serializer.save(author=default_author)
