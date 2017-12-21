from django.db import models
from django.db.models.signals import pre_save,post_save
from django.urls import reverse
from django.utils import timezone
from blog.utils import unique_slug_generator
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from comments.models import Comment
# Create your models here.
def upload_location(instance,filename):
	return "%s/%s" % (instance.id,filename)






class Post(models.Model):
	user  = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
	title = models.CharField(max_length=120)
	slug  =models.SlugField(unique=True,blank=True)
	image = models.ImageField(upload_to=upload_location,blank=True,null=True,width_field="width_field",height_field="height_field")
	width_field=models.IntegerField(default=0)
	height_field=models.IntegerField(default=0)
	content = models.TextField()
	description = models.CharField(max_length=120)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.title

	class Meta:
		ordering=['-timestamp','-updated']

	def get_absolute_url(self):
		return reverse('posts:detail',kwargs={'slug':self.slug})

	@property
	def comments(self):
		instance=self
		qs=Comment.objects.filter_by_instance(instance)
		return qs
	@property
	def get_content_type(self):
		instance=self
		return ContentType.objects.get_for_model(instance)

def pre_save_post_receiver(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug=unique_slug_generator(instance)
pre_save.connect(pre_save_post_receiver,sender=Post)

