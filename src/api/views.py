
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from .models import Project, Issue, Comment, Contributor
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from .permissions import IsAuthorOrReadOnly, IsContributorOrAuthor

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    #permission_classes = [IsAuthenticated, IsContributorOrAuthor] 

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            # Les administrateurs voient tous les projets
            return Project.objects.all()
        else:
            # Les utilisateurs voient les projets dont ils sont auteurs ou contributeurs
            # Récupérer les IDs des projets auxquels l'utilisateur contribue
            contributed_project_ids = Contributor.objects.filter(user=user).values_list('project_id', flat=True)
            # Retourner les projets dont l'utilisateur est auteur ou contributeur
            return Project.objects.filter(
                Q(author=user) | Q(id__in=contributed_project_ids)
            ).distinct()
    
    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated, IsContributorOrAuthor]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]    
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        # Ajouter automatiquement l'auteur comme contributeur du projet
        Contributor.objects.create(user=self.request.user, project=project)

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributorOrAuthor, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ContributorViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing contributor instances.
    """
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsContributorOrAuthor]

    def get_queryset(self):
        """
        This view should return a list of all the contributors for
        the project as determined by the project id in the URL.
        """
        project_id = self.kwargs.get('project_pk', None)
        return Contributor.objects.filter(project__id=project_id)

    def perform_create(self, serializer):
        """
        Ensure the user adding a contributor is the project author.
        """
        project_id = self.kwargs.get('project_pk', None)
        project = Project.objects.get(pk=project_id)

        if project.author != self.request.user:
            raise PermissionDenied("Seul l'auteur du projet peut ajouter des contributeurs..")

        serializer.save(project=project)