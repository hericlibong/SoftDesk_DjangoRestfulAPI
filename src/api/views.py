from rest_framework.viewsets import ModelViewSet
from .models import Project, Contributor, Issue, Comment
from .serializers import (ProjectSerializer, ContributorSerializer, 
                          CommentSerializer, IssueSerializer)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthor, IsContributor, IsAuthorOrReadOnly


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.prefetch_related('contributors', 'issues')  # Précharge les relations
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]
    ordering_fields = ['-created_time']

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionError("You must be authenticated to create a project.")
        serializer.save(author=self.request.user)
    


class ContributorViewSet(ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsContributor, IsAuthenticated]

    def get_queryset(self):
        # Vérifie si 'project_pk' est présent dans les kwargs
        project_id = self.kwargs.get('project_pk', None)
        if project_id:
            # si oui, le projet est précisé et on filtre les contributeurs par projet
            return Contributor.objects.filter(project__id=project_id)
        else:
            # sinon on retourne tous les contributeurs
            return Contributor.objects.all()
    

class IssueViewSet(ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # Assigner l'utilisateur authentifié comme auteur
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # Vérifie si 'project_pk' est présent dans les kwargs
        project_id = self.kwargs.get('project_pk', None)
        if project_id:
            # si oui, le projet est précisé et on filtre les contributeurs par projet
            return Issue.objects.filter(project__id=project_id)
        else:
            # sinon on retourne tous les contributeurs
            return Issue.objects.all()


class CommentViewSet(ModelViewSet): 
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionError("You must be authenticated to create a project.")
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # Vérifie si 'issue_pk' est présent dans les kwargs
        issue_id = self.kwargs.get('issue_pk', None)
        if issue_id:
            # si oui, l'issue est précisée et on filtre les commentaires par issue
            return Comment.objects.filter(issue__id=issue_id)
        else:
            # sinon on retourne tous les commentaires
            return self.queryset
