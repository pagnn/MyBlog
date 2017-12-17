from django.db import models
from django.db.models.signals import pre_save,post_save
from django.urls import reverse
from blog.utils import unique_slug_generator
# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=120)
	slug  =models.SlugField(unique=True,blank=True)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('posts:detail',kwargs={'slug':self.slug})

def pre_save_post_receiver(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug=unique_slug_generator(instance)
pre_save.connect(pre_save_post_receiver,sender=Post)

