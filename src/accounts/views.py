from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    
    def destroy(self, request, *args, **kwargs):
        # écrire un message quand un utilisateur est supprimé
        user = self.get_object()
        user.delete()
        return Response({"message": "L'utilisateur a été supprimé avec succès"}, status=status.HTTP_200_OK)
      
