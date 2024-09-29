
from rest_framework.permissions import BasePermission
from .models import Contributor, Issue, Comment


class IsAuthor(BasePermission):
    """
    Permisssion qui permet à l'auteur d'un objet d'y accéder 
    
    """
    message = "Vous devez être l'auteur de cette ressource pour y accéder"

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    

class IsContributor(BasePermission):
    """
    Permission qui permet à un contributeur d'accéder aux projets, issues et commentaires.
    """
    message = "Vous devez être contributeur de ce projet pour accéder à cette ressource."

    def has_permission(self, request, view):
        project_id = (
            view.kwargs.get('project_pk') or
            self.get_project_id_from_issue(view) or
            self.get_project_id_from_comment(view)
        )
        if not project_id:
            return False
        return Contributor.objects.filter(project_id=project_id, user=request.user).exists()

    def get_project_id_from_issue(self, view):
        issue_id = view.kwargs.get('issue_pk') or view.kwargs.get('issue_id')
        if issue_id:
            try:
                issue = Issue.objects.get(id=issue_id)
                return issue.project.id
            except Issue.DoesNotExist:
                return None
        return None

    def get_project_id_from_comment(self, view):
        comment_id = view.kwargs.get('pk')
        if comment_id:
            try:
                comment = Comment.objects.get(id=comment_id)
                return comment.issue.project.id
            except Comment.DoesNotExist:
                return None
        return None

    