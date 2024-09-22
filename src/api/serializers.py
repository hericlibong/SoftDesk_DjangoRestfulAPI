from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment
from django.contrib.auth import get_user_model


# Serializer for Contributor model
class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    # project = serializers.StringRelatedField()

    class Meta:
        model = Contributor
        fields = ['id', 'user']
        read_only_fields = ['id']


# Serializer for Comment model
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    issue = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'created_time', 'issue']
        read_only_fields = ['id', 'author', 'created_time', 'issue']


# Serializer for Issue model
class IssueSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.title', read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    author_name = serializers.CharField(source='author.username', read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'project_name', 'project', 'assigned_to_name',
                  'assigned_to', 'status', 'priority', 'tag',
                  'author_name', 'author', 'created_time', 'comments']
        read_only_fields = ['id', 'author', 'created_time', 'comments']
        extra_kwargs = {
            'comments': {'required': False}
        }


# Serializer for Project model
class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    # Utilise une méthode personnalisée pour sérialiser les contributeurs avec des détails
    contributors = serializers.SerializerMethodField()

    # Sérialisation des issues associées
    issues = IssueSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type',
                  'created_time', 'author', 'contributors', 'issues']
        read_only_fields = ['id', 'created_time', 'author']

    def get_contributors(self, obj):
        """
        Récupère et sérialise les contributeurs d'un projet donné.
        """
        contributors = Contributor.objects.filter(project=obj)
        return ContributorSerializer(contributors, many=True).data
