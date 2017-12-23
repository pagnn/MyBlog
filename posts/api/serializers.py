from rest_framework.serializers import ModelSerializer

from posts.models import Post 


class PostCreateSerializer(ModelSerializer):
	class Meta:
		model=Post
		fields=[
			'title',
			'description',
			'content'
		]	
class PostListSerializer(ModelSerializer):
	class Meta:
		model=Post
		fields=[
			'user',
			'title',
			'description',
			'content',
			'slug'
		]

class PostDetailSerializer(ModelSerializer):
	class Meta:
		model=Post
		fields=[
			'title',
			'description',
			'content',
		]	