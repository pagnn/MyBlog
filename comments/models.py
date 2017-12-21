from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.
from django.conf import settings




class CommentManager(models.Manager):
	def filter_by_instance(self,instance):
		object_id=instance.id
		content_type=ContentType.objects.get_for_model(instance.__class__)
		qs=super(CommentManager,self).filter(content_type=content_type,object_id=object_id)
		return qs

class Comment(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,null=True)
	object_id = models.PositiveIntegerField(null=True)
	content_object = GenericForeignKey('content_type', 'object_id')
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	objects=CommentManager()

	def __str__(self):
		return str(self.user.username)

