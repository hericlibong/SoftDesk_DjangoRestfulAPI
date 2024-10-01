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
    """Permet uniquement aux administrateurs, aux contributeurs ou à l'auteur d'accéder aux ressources du projet."""

    def has_object_permission(self, request, view, obj):
        # Les utilisateurs administrateurs peuvent accéder à toutes les ressources
        if request.user.is_staff:
            return True
        
       
        # Vérifie si l'objet a un attribut 'author' et si l'auteur de l'objet est l'utilisateur actuel
        if hasattr(obj, 'author') and obj.author == request.user:
            # Si c'est le cas, l'utilisateur a la permission d'accéder à l'objet
            return True

        
        # Vérifie si l'objet est une instance de la classe Project
        if isinstance(obj, Project):
            project = obj
        # Si l'objet a un attribut 'project', assigne cet attribut à la variable project
        elif hasattr(obj, 'project'):
            project = obj.project
        # Si aucune des conditions précédentes n'est remplie, retourne False
        else:
            return False  

        # Seuls les contributeurs ou l'auteur de l'objet peuvent accéder à la ressource
        # return obj.author == request.user or request.user in obj.contributors.all()
        return Contributor.objects.filter(user=request.user, project=project).exists()

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
