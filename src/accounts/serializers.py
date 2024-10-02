from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email',
                  'age', 'can_be_contacted', 'can_be_data_shared', 'groups', 'user_permissions']
        read_only_fields = ['id', 'groups', 'user_permissions']
        extra_kwargs = {
            'groups': {'required': False},
            'user_permissions': {'required': False},
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data.get('age') is not None and data['age'] < 15:
            raise serializers.ValidationError("l'utilisateur doit avoir au moins 15 ans pour s'inscrire")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            age=validated_data.get('age'),
            can_be_contacted=validated_data.get('can_be_contacted', False),
            can_be_data_shared=validated_data.get('can_be_data_shared', False)
        )
        return user
