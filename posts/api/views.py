from rest_framework.generics import ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView,CreateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination
from posts.models import Post 
from .serializers import PostListSerializer,PostDetailSerializer,PostCreateSerializer
from .permissions import IsOwnerOrReadOnly
from .paginations import PostLimitOffsetPagination,PostPageNumberPagination
class PostListAPIView(ListAPIView):
	pagination_class=PostPageNumberPagination
	serializer_class=PostListSerializer
	def get_queryset(self,*args,**kwargs):
		queryset=Post.objects.filter(user=self.request.user)
		return queryset

class PostDetailAPIView(RetrieveAPIView):
	queryset=Post.objects.all()
	serializer_class=PostDetailSerializer	
	lookup_field='slug'


class PostUpdateAPIView(UpdateAPIView):
	queryset=Post.objects.all()
	serializer_class=PostDetailSerializer	
	lookup_field='slug'
	permission_classes=[IsOwnerOrReadOnly,IsAdminUser]
class PostDeleteAPIView(DestroyAPIView):
	queryset=Post.objects.all()
	serializer_class=PostDetailSerializer	
	lookup_field='slug'
	permission_classes=[IsOwnerOrReadOnly,IsAdminUser]
class PostCreateAPIView(CreateAPIView):
	queryset=Post.objects.all()
	serializer_class=PostCreateSerializer
	permission_classes=[IsOwnerOrReadOnly,IsAdminUser]
	def perform_create(self,serializer):
		serializer.save(user=self.request.user)