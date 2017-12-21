from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.
from posts.models import Post

class CommentManager(models.Manager):
	def all(self):
		qs=super(CommentManager,self).filter(parent=None)
		return qs

class Comment(models.Model):
	email = models.EmailField(default='findpagnn@gmail.com')
	post  = models.ForeignKey(Post,on_delete=models.CASCADE,default=1)
	content = models.CharField(max_length=150)
	timestamp = models.DateTimeField(auto_now_add=True)
	parent =models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)

	objects = CommentManager()
	def __str__(self):
		return str(self.email)

	
	def children(self):
		return Comment.objects.filter(parent=self)

	@property
	def is_parent(self):
		if self.parent is None:
			return False
		return True
