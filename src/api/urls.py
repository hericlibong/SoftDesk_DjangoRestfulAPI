# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet

# Routeur principal
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'contributors', ContributorViewSet, basename='contributor')
router.register(r'issues', IssueViewSet, basename='issue')
router.register(r'comments', CommentViewSet, basename='comment')

# Routeur imbriqué pour les contributeurs par projet
projects_contributors_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
projects_contributors_router.register(r'contributors', ContributorViewSet, basename='project-contributors')

# Routeur imbriqué pour les issues par projet
projects_issues_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
projects_issues_router.register(r'issues', IssueViewSet, basename='project-issues')

# Routeur imbriqué pour les issues par contributeur
contributors_issues_router = routers.NestedDefaultRouter(router, r'contributors', lookup='contributor')
contributors_issues_router.register(r'issues', IssueViewSet, basename='contributor-issues')

# Routeur imbriqué pour les commentaires par issue
issues_comments_router = routers.NestedDefaultRouter(router, r'issues', lookup='issue')
issues_comments_router.register(r'comments', CommentViewSet, basename='issue-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_contributors_router.urls)),
    path('', include(projects_issues_router.urls)),
    path('', include(contributors_issues_router.urls)),
    path('', include(issues_comments_router.urls)),
]


