from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

from posts.models import Post
User=get_user_model()

class PostAPITestCase(APITestCase):
	def setUp(self):
		user_obj=User(username='testuser',email='testuser@gmail.com')
		user_obj.set_password('testuser2017')
		user_obj.save()
		post_obj=Post.objects.create(
				user=user_obj,
				title='new title',
				content='new content',
				description='new description')

	def test_single_user(self):
		user_count=User.objects.count()
		self.assertEqual(user_count,1)

	def test_single_post(self):
		post_count=Post.objects.count()
		self.assertEqual(post_count,1)	