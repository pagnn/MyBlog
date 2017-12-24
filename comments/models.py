from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy,reverse
# Create your models here.
from posts.models import Post

class CommentManager(models.Manager):
	def all(self):
		qs=super(CommentManager,self).filter(parent=None)
		return qs
	def create_by_model_type(self,model_type,slug,email,content,parent_obj=None):
		model_qs=ContentType.objects.filter(model=model_type)
		if model_qs.exists():
			somemodel=model_qs.first().model_class()
			obj_qs=somemodel.objects.filter(slug=slug)
			if obj_qs.exists() and obj_qs.count() == 1:
				instance=self.model()
				instance.content=content
				instance.email=email
				instance.post=obj_qs.first()
				if parent_obj:
					instance.parent=parent_obj
				instance.save()
				return instance
		return None

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
			return True
		return False
	def get_absolute_url(self):
		return reverse('comments:thread',kwargs={'pk':self.pk})
