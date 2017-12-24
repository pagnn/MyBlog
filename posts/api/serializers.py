from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField,SerializerMethodField

from posts.models import Post 
from comments.models import Comment
from comments.api.serializers import CommentListSerializer
from accounts.api.serializers import UserDetailSerializer
class PostCreateSerializer(ModelSerializer):
	class Meta:
		model=Post
		fields=[
			'title',
			'description',
			'content'
		]	
class PostListSerializer(ModelSerializer):
	url=HyperlinkedIdentityField(
			view_name='posts-api:detail',
			lookup_field='slug'
		)
	user=UserDetailSerializer(read_only=True)
	class Meta:
		model=Post
		fields=[
			'url',
			'user',
			'title',
			'description',
			'content'
		]

class PostDetailSerializer(ModelSerializer):
	image=SerializerMethodField()
	comments=SerializerMethodField()
	class Meta:
		model=Post
		fields=[
			'title',
			'description',
			'content',
			'image',
			'comments'
		]
	def get_comments(self,obj):
		comments=Comment.objects.filter(post=obj)
		if comments.exists():
			comments=CommentListSerializer(comments,many=True).data
		else:
			comments=None
		return comments

	def get_image(self,obj):
		try:
			image=obj.image.url
		except:
			image = None
		return image