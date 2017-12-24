from rest_framework.generics import ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView,CreateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.mixins import DestroyModelMixin,UpdateModelMixin

from django.contrib.auth import get_user_model

from .serializers import UserCreateSerializer

User=get_user_model()
class UserCreateAPIView(CreateAPIView):
	queryset=User.objects.all()
	serializer_class=UserCreateSerializer