from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment
from django.contrib.auth import get_user_model


# Serializer for Contributor model
class ContributorSerializer(serializers.ModelSerializer):
    contributor_username = serializers.CharField(source='user.username', read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'contributor_username']
        read_only_fields = ['id', 'contributor_username']


# Serializer for Comment model
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    issue = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'created_time', 'issue']
        read_only_fields = ['id', 'author', 'created_time', 'issue']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Nettoyer les retours à la ligne
        representation['description'] = representation['description'].replace(
            '\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
        return representation


# Serializer for Issue model
class IssueSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.title', read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    author_name = serializers.CharField(source='author.username', read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    # comments = CommentSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'project_name', 'project', 'assigned_to_name',
                  'assigned_to', 'status', 'priority', 'tag',
                  'author_name', 'author', 'created_time', 'comments']
        read_only_fields = ['id', 'author', 'created_time', 'comments']
        extra_kwargs = {
            'comments': {'required': False}
        }

    def validate_assigned_to(self, value):
        """
        Vérifie que le contributeur assigné fait partie des contributeurs du projet.
        - value: l'utilisateur assigné à l'issue
        """
        # Récupérer le projet à partir du contexte
        project = self.context.get('project')
        if not project:
            raise serializers.ValidationError("Le projet n'est pas disponible dans le contexte.")

        # Vérifier si l'utilisateur assigné fait partie des contributeurs du projet
        if not Contributor.objects.filter(project=project, user=value).exists():
            # Si l'utilisateur n'est pas un contributeur du projet, lever une erreur de validation
            raise serializers.ValidationError("Le contributeur assigné doit être un contributeur du projet")

        # Si l'utilisateur est un contributeur valide, retourner la valeur
        return value

    def get_comments(self, obj):
        """
        Récupère et renvoie uniquement les descriptions des commentaires.
        """
        comments = Comment.objects.filter(issue=obj)
        return [{'id': comment.id, 'created_time': comment.created_time} for comment in comments]


# Serializer for Project model
class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    # Utilise une méthode personnalisée pour sérialiser les contributeurs avec des détails
    contributors = serializers.SerializerMethodField()

    # Sérialisation des issues associées
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type',
                  'created_time', 'author', 'contributors', 'issues']
        read_only_fields = ['id', 'created_time', 'author']

    def get_contributors(self, obj):
        """
        Récupère et renvoie uniquement les noms des contributeurs.
        """
        contributors = Contributor.objects.filter(project=obj).select_related('user')
        # return ContributorSerializer(contributors, many=True).data
        return [{'id': contributor.id, 'name': contributor.user.username, 'user_id': contributor.user.id}
                for contributor in contributors]

    def get_issues(self, obj):
        """
        Récupère et renvoie uniquement les titres des issues.
        """
        issues = Issue.objects.filter(project=obj).prefetch_related('comments')  # Précharger les commentaires
        # return IssueSerializer(issues, many=True).data
        # return [{'id': issue.id, 'title': issue.title, 'comments': issue.comments.count()} for issue in issues]
        issues_data = []
        for issue in issues:
            issue_comments = [{'id': comment.id, 'description': comment.description,
                               'author': comment.author.username} for comment in issue.comments.all()]
            issues_data.append({
                'id': issue.id,
                'title': issue.title,
                'author': issue.author.username,
                'nb_comments': len(issue_comments),
                'comments': issue_comments
            })
        return issues_data
