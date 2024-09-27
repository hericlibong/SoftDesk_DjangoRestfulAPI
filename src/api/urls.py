from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet 

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'contributors', ContributorViewSet, basename='contributor')
router.register(r'issues', IssueViewSet, basename='issue')
router.register(r'comments', CommentViewSet, basename='comment')

# Create a nested router for projects
projects_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
# Register the IssueViewSet with the nested projects router
projects_router.register(r'issues', IssueViewSet, basename='project-issues')

# Create a nested router for issues within projects
issue_router = routers.NestedDefaultRouter(projects_router, r'issues', lookup='issue')
# Register the CommentViewSet with the nested issues router
issue_router.register(r'comments', CommentViewSet, basename='issue-comments')

issue_router_comment  = routers.NestedDefaultRouter(router, r'issues', lookup='comment')
issue_router_comment.register(r'comments', CommentViewSet, basename='issue-comment')

# Register the ContributorViewSet with the nested projects router
projects_router.register(r'contributors', ContributorViewSet, basename='project-contributors')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('', include(issue_router.urls)),
    path('', include(issue_router_comment.urls)),
]



