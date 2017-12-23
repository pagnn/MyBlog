from rest_framework.generics import ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView,CreateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from posts.models import Post 
from .serializers import PostListSerializer,PostDetailSerializer,PostCreateSerializer

class PostListAPIView(ListAPIView):
	queryset=Post.objects.all()
	serializer_class=PostListSerializer


class PostDetailAPIView(RetrieveAPIView):
	queryset=Post.objects.all()
	serializer_class=PostDetailSerializer	
	lookup_field='slug'

class PostUpdateAPIView(UpdateAPIView):
	queryset=Post.objects.all()
	serializer_class=PostDetailSerializer	
	lookup_field='slug'
class PostDeleteAPIView(DestroyAPIView):
	queryset=Post.objects.all()
	serializer_class=PostDetailSerializer	
	lookup_field='slug'
class PostCreateAPIView(CreateAPIView):
	queryset=Post.objects.all()
	serializer_class=PostCreateSerializer
	def perform_create(self,serializer):
		serializer.save(user=self.request.user)
		return 