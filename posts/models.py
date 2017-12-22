from django.db import models
from django.db.models.signals import pre_save,post_save
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from markdown_deux import markdown


from blog.utils import unique_slug_generator,get_read_time
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
	read_time=models.TimeField(null=True,blank=True)
	description = models.CharField(max_length=120)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.title

	class Meta:
		ordering=['-timestamp','-updated']

	def get_absolute_url(self):
		return reverse('posts:detail',kwargs={'slug':self.slug})
	def get_markdown(self):
		content=self.content
		markdown_content=markdown(content)
		return mark_safe(markdown_content)
	@property
	def comments(self):
		instance=self
		qs=self.comment_set.all()
		return qs
		

def pre_save_post_receiver(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug=unique_slug_generator(instance)
	if instance.content:
		html_string=instance.get_markdown()
		read_time=get_read_time(html_string)
		instance.read_time=read_time

pre_save.connect(pre_save_post_receiver,sender=Post)

