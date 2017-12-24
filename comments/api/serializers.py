from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField,SerializerMethodField,ValidationError
from django.contrib.contenttypes.models import ContentType


from comments.models import Comment



def create_comment_serializer(model_type='post',slug=None,parent_id=None):
	class CommentCreateSerializer(ModelSerializer):
		class Meta:
			model=Comment
			fields=[
				'email',
				'content'
			]
		def __init__(self,*args,**kwargs):
			self.model_type=model_type
			self.slug=slug
			self.parent_obj=None
			if parent_id:
				parent_qs=Comment.objects.filter(id=parent_id)
				if parent_qs.exists() and parent_qs.count() == 1:
					self.parent_obj=parent_qs.first()

			return super(CommentCreateSerializer,self).__init__(*args,**kwargs)
		def validate(self,data):
			model_type=self.model_type
			model_qs=ContentType.objects.filter(model=model_type)
			if not model_qs.exists():
				raise ValidationError('This is not a valid content type.')
			someModel=model_qs.first().model_class()
			obj_qs=someModel.objects.filter(slug=self.slug)
			if not obj_qs.exists() or obj_qs.count() != 1:
				raise ValidationError('This is not a valid slug.')
			return data
		def create(self,validated_data):
			content=validated_data.get('content')
			email=validated_data.get('email')
			model_type=self.model_type
			slug=self.slug
			parent_obj=self.parent_obj
			comment=Comment.objects.create_by_model_type(
				model_type=model_type,
				slug=slug,
				email=email,
				content=content,
				parent_obj=parent_obj)
			return comment
	return CommentCreateSerializer

class CommentListSerializer(ModelSerializer):
	replycount=SerializerMethodField()
	url=HyperlinkedIdentityField(
			view_name='comments-api:detail',
			lookup_field='pk'
		)
	class Meta:
		model=Comment
		fields=[
			'url',
			'email',
			'post',
			'content',
			'replycount'
		]
	def get_replycount(self,obj):
		if obj.is_parent:
			return obj.children().count()
		return 0

class CommentChildDetailSerializer(ModelSerializer):
	class Meta:
		model=Comment
		fields=[
			'email',
			'content',
			'timestamp'
		]
class CommentDetailSerializer(ModelSerializer):
	replies=SerializerMethodField()
	post_url=SerializerMethodField()
	class Meta:
		model=Comment
		fields=[
			'email',
			'post_url',
			'content',
			'replies',
			'timestamp'
		]
		read_only_fields=[
			'email',
			'replies',
			'timestamp'
		]
	def get_replies(self,obj):
		if obj.is_parent:
			return CommentChildDetailSerializer(obj.children(),many=True).data
		return None
	def get_post_url(self,obj):
		return obj.post.get_api_absolute_url()
