from rest_framework import serializers
# from django.contrib.auth.models import Group
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'age', 'can_be_contacted', 'can_be_data_shared', 'groups', 'user_permissions']
        read_only_fields = ['id']
        extra_kwargs = {
            'groups': {'required': False},
            'user_permissions': {'required': False}, 
            'password': {'write_only': True}
        }

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
    
# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['id', 'name']
#         read_only_fields = ['id']