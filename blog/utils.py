import datetime
import re
import math
import string
import random
from django.utils.text import slugify
from django.utils.html import strip_tags
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


def count_words(html_string):
	word_string=strip_tags(html_string)
	count=len(re.findall(r'\w+',word_string))
	return count
def get_read_time(html_string):
	count=count_words(html_string)
	print(count)
	read_time_min=math.ceil(count/200.0)
	read_time=str(datetime.timedelta(minutes=read_time_min))
	return read_time
