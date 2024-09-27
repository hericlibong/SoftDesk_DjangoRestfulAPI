from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import Contributor


class IsAuthor(BasePermission):
    """
    Permisssion qui permet à l'auteur d'un objet d'y accéder 
    
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    
class IsContributor(BasePermission):
    """
    Permisssion qui permet à un contributeur d'un projet d'accéder aux issues, 
    aux commentaires et d'être assigné à une issue
    
    """
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_pk')
        return Contributor.objects.filter(project__id=project_id, user=request.user).exists()
    

class IsAuthorOrReadOnly(BasePermission):
    """
    Permisssion qui permet à l'auteur d'un objet de le modifier ou de le supprimer
    
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user