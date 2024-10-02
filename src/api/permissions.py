from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Project, Contributor

class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow authors of a resource to edit or delete it.
    All users can view the resource if they have the appropriate access.
    """

    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to any request, so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author of the object.
        return obj.author == request.user or request.user.is_staff


class IsContributorOrAuthor(BasePermission):
    """
    Permet uniquement aux administrateurs, aux contributeurs ou à l'auteur d'accéder aux ressources du projet.
    """

    def has_permission(self, request, view):
        # Les administrateurs ont accès à tout
        if request.user.is_staff:
            return True

        # Pour les actions qui ne nécessitent pas de projet spécifique (e.g., list), on permet l'accès
        # et on laisse le get_queryset filtrer les résultats
        if view.action in ['list', 'create']:
            return True

        # Récupérer l'ID du projet depuis les paramètres de l'URL
        project_id = view.kwargs.get('project_pk') or view.kwargs.get('project_id')

        if not project_id:
            # Si nous ne pouvons pas déterminer le projet, nous permettons l'accès
            # La méthode has_object_permission s'occupera du reste
            return True

        # Vérifier si l'utilisateur est contributeur ou auteur du projet
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return False

        if project.author == request.user:
            return True

        return Contributor.objects.filter(project=project, user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        # Les administrateurs ont accès à tout
        if request.user.is_staff:
            return True

        # Vérifier si l'utilisateur est l'auteur de l'objet
        if hasattr(obj, 'author') and obj.author == request.user:
            return True

        # Vérifier si l'objet a un projet associé
        if hasattr(obj, 'project'):
            project = obj.project
        else:
            # Si l'objet est un projet, on l'utilise directement
            project = obj

        # Vérifier si l'utilisateur est l'auteur ou contributeur du projet
        if project.author == request.user:
            return True

        return Contributor.objects.filter(project=project, user=request.user).exists()

class IsAuthenticatedAndContributor(BasePermission):
    """
    Permission to check if a user is authenticated and is a contributor to the project.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Retrieve the project from the request (adjust depending on your view setup)
        project = view.get_object()

        # Check if the user is a contributor
        return request.user in project.contributors.all()
