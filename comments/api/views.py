from rest_framework.generics import ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView,CreateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.mixins import DestroyModelMixin,UpdateModelMixin

from .serializers import CommentListSerializer,CommentDetailSerializer,create_comment_serializer
from comments.models import Comment
from .permissions import IsOwnerOrReadOnly

class CommentCreateAPIView(CreateAPIView):
	queryset=Comment.objects.all()
	permission_classes=[IsOwnerOrReadOnly,IsAdminUser]
	def get_serializer_class(self):
		model_type=self.request.GET.get('type')
		slug=self.request.GET.get('slug')
		parent_id=self.request.GET.get('parent_id')
		return create_comment_serializer(model_type=model_type,slug=slug,parent_id=parent_id)
class CommentListAPIView(ListAPIView):
	serializer_class=CommentListSerializer
	def get_queryset(self,*args,**kwargs):
		queryset=Comment.objects.all()
		return queryset

class CommentDetailAPIView(DestroyModelMixin,UpdateModelMixin,RetrieveAPIView):
	queryset=Comment.objects.filter(id__gte=0)
	serializer_class=CommentDetailSerializer
	permission_classes=[IsOwnerOrReadOnly,IsAdminUser]

	def put(self,request,*args,**kwargs):
		return self.updated(request,*args,**kwargs)
	def delete(self,request,*args,**kwargs):
		return self.destroy(request,*args,**kwargs)		