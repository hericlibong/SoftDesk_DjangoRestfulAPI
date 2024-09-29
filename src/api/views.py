from rest_framework.viewsets import ModelViewSet
from .models import Project, Contributor, Issue, Comment
from .serializers import (ProjectSerializer, ContributorSerializer, 
                          CommentSerializer, IssueSerializer)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthor, IsContributor


class ProjectViewSet(ModelViewSet):
    # Précharge les contributeurs et les problèmes associés pour optimiser les requêtes
    queryset = Project.objects.prefetch_related('contributors', 'issues')
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated, IsContributor]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        # Récupère l'identifiant du projet à partir des arguments de l'URL
        project_id = self.kwargs.get('project_pk', None)
        if project_id:
            return Contributor.objects.filter(project__id=project_id) 
        else:  
            return Contributor.objects.all()
        
    def get_permissions(self):
        # Si l'action est 'create' ou 'destroy' définir les permissions pour les utilisateurs authentifiés et les auteurs
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthor]
        elif self.action in ['retrieve', 'list']:  # Si l'action est 'retrieve' ou 'list', définir les permissions pour les utilisateurs authentifiés et les contributeurs du projet
            permission_classes = [IsAuthenticated, IsContributor]
        else:
            # Pour toutes les autres actions, définir les permissions pour les utilisateurs authentifiés et les contributeurs du projet
            permission_classes = [IsAuthenticated]
        # Retourner une instance de chaque classe de permission
        return [permission() for permission in permission_classes]
    


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk', None)
        contributor_id = self.kwargs.get('contributor_pk', None)
        if project_id:
            return Issue.objects.filter(project__id=project_id)
        elif contributor_id:
            return Issue.objects.filter(assigned_to__id=contributor_id)
        else:
            return Issue.objects.all()
        
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsContributor]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated, IsContributor]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        if project_id:
            project = Project.objects.get(id=project_id)
            serializer.save(author=self.request.user, project=project)
        else:
            serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        issue_id = self.kwargs.get('issue_pk')
        if issue_id:
            return Comment.objects.filter(issue__id=issue_id)
        else:
            return Comment.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsContributor]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated, IsContributor]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        issue_id = self.kwargs.get('issue_pk')
        if issue_id:
            issue = Issue.objects.get(id=issue_id)
            serializer.save(author=self.request.user, issue=issue)
        else:
            serializer.save(author=self.request.user)
