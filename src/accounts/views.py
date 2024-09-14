from .models import User
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication] 
    
      
