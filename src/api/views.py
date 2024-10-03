from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Project, Issue, Comment, Contributor
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from .permissions import IsAuthorOrReadOnly, IsContributorOrAuthor


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsContributorOrAuthor]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            # Les administrateurs voient tous les projets
            return Project.objects.all()
            # return Project.objects.select_related('author').prefetch_related('contributor').all()
        else:
            # Les utilisateurs voient les projets dont ils sont auteurs ou contributeurs
            # Récupérer les IDs des projets auxquels l'utilisateur contribue
            contributed_project_ids = Contributor.objects.filter(user=user).values_list('project_id', flat=True)
            # Retourner les projets dont l'utilisateur est auteur ou contributeur
            return Project.objects.filter(
                Q(author=user) | Q(id__in=contributed_project_ids)
            ).distinct()
            # return Project.objects.select_related('author').prefetch_related('contributor').filter(
            #     Q(author=user) | Q(id__in=contributed_project_ids)
            # ).distinct()

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

    def get_object(self):
        # Récupérer le projet indépendament des permissions
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        # project = get_object_or_404(
        #     Project.objects.select_related('author').prefetch_related('contributor'),
        #     pk=self.kwargs.get('pk')
        # )

        # Vérifier les permissions sur l'objet
        self.check_object_permissions(self.request, project)

        return project

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributorOrAuthor]

    def get_queryset(self):
        user = self.request.user
        project_id = self.kwargs.get('project_pk')

        if project_id:
            # Cas où le project_id est spécifié dans l'URL
            queryset = Issue.objects.filter(project__id=project_id)
        else:
            # Cas où le project_id n'est pas spécifié
            # Récupérer les projets auxquels l'utilisateur a accès
            user_projects = Project.objects.filter(
                Q(author=user) |
                Q(contributor__user=user)
            ).distinct()

            # Récupérer les Issues de ces projets
            queryset = Issue.objects.filter(project__in=user_projects)

        return queryset

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        if project_id:
            project = Project.objects.get(pk=project_id)
            serializer.save(author=self.request.user, project=project)
        else:
            # Si aucun project_id n'est fourni, interdire la création
            raise PermissionDenied("Vous ne pouvez pas créer une Issue sans spécifier un projet.")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        project_id = self.kwargs.get('project_pk')
        if project_id:
            project = Project.objects.get(pk=project_id)
            context['project'] = project
        return context


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsContributorOrAuthor]

    def get_queryset(self):
        user = self.request.user
        project_id = self.kwargs.get('project_pk')
        issue_id = self.kwargs.get('issue_pk')

        if project_id and issue_id:
            # Vérifier que l'utilisateur a accès au projet et à l'issue
            project = get_object_or_404(Project, pk=project_id)
            issue = get_object_or_404(Issue, pk=issue_id, project=project)

            # Vérifier les permissions
            if not (project.author == user or Contributor.objects.filter(project=project, user=user).exists()):
                return Comment.objects.none()

            return Comment.objects.filter(issue=issue)
        else:
            # Si project_id ou issue_id n'est pas fourni, retourner tous les commentaires accessibles
            user_projects = Project.objects.filter(
                Q(author=user) |
                Q(contributor__user=user)
            ).distinct()
            issues = Issue.objects.filter(project__in=user_projects)
            return Comment.objects.filter(issue__in=issues)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        issue_id = self.kwargs.get('issue_pk')

        project = get_object_or_404(Project, pk=project_id)
        issue = get_object_or_404(Issue, pk=issue_id, project=project)

        user = self.request.user

        # Si l'utilisateur est un administrateur, autorisez la création de commentaire
        if user.is_staff:
            serializer.save(author=user, issue=issue)
            return

        # Vérifiez que l'utilisateur est l'auteur du projet ou un contributeur
        if not (project.author == user or Contributor.objects.filter(project=project, user=user).exists()):
            raise PermissionDenied("Vous n'êtes pas autorisé à commenter cette issue.")

        # Enregistrez le commentaire si toutes les conditions sont remplies
        serializer.save(author=user, issue=issue)


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsContributorOrAuthor]

    def get_queryset(self):
        user = self.request.user
        project_id = self.kwargs.get('project_pk')

        if user.is_staff:
            return Contributor.objects.filter(project__id=project_id)

        if project_id:
            # Cas où le project_id est spécifié dans l'URL
            queryset = Contributor.objects.filter(project__id=project_id)
        else:
            # Cas où le project_id n'est pas spécifié
            # Récupérer les projets auxquels l'utilisateur a accès
            user_projects = Project.objects.filter(
                Q(author=user) |
                Q(contributor__user=user)
            ).distinct()

            # Récupérer les contributeurs de ces projets
            queryset = Contributor.objects.filter(project__in=user_projects)

        return queryset

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        if project_id:
            project = Project.objects.get(pk=project_id)
            if project.author != self.request.user:
                raise PermissionDenied("Seul l'auteur du projet peut ajouter des contributeurs.")
            serializer.save(project=project)
        else:
            # Si aucun project_id n'est fourni, interdire la création
            raise PermissionDenied("Vous ne pouvez pas créer un contributeur sans spécifier un projet.")
