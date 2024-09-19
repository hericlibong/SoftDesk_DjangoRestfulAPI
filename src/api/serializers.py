from rest_framework import serializers
from .models import Project, Contributor


class ProjectSerializer(serializers.ModelSerializer):       
    author = serializers.StringRelatedField()
    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'created_time', 'author', 'contributors']
        read_only_fields = ['id', 'created_time', 'author']
        extra_kwargs = {
            'contributors': {'required': False}
        }

    def get_contributors(self, obj):
        """
        Récupère et sérialise les contributeurs d'un projet donné.
        """
        contributors = Contributor.objects.filter(project=obj)
        return ContributorSerializer(contributors, many=True).data

class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    # project = serializers.StringRelatedField()

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']
        read_only_fields = ['id']
        
