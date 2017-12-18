import string
import random
from django.utils.text import slugify
def random_string(size=4,chars=string.ascii_lowercase+string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance,new_slug=None):
	if new_slug is None:
		new_slug=slugify(instance.title)
	else:
		new_slug=new_slug
	klass=instance.__class__
	qs=klass.objects.filter(slug=new_slug)
	if qs.exists():
		new_slug="{slug}-{randstr}".format(slug=new_slug,randstr=random_string(size=4))
		return unique_slug_generator(instance,new_slug)
	return new_slug