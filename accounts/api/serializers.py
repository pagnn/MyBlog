from rest_framework.serializers import EmailField,CharField,ModelSerializer,HyperlinkedIdentityField,SerializerMethodField,ValidationError


from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q
User=get_user_model()

class UserDetailSerializer(ModelSerializer):
	class Meta:
		model=User
		fields=[
			'username',
			'email'
		]
class UserLoginSerializer(ModelSerializer):
	token=CharField(allow_blank=True,read_only=True)
	email=EmailField(required=False,allow_blank=True)
	username=CharField(required=False,allow_blank=True)
	class Meta:
		model=User
		fields=[
			'username',
			'email',
			'password',
			'token'
		]
	def validate(self,data):
		email=data.get('email',None)
		username=data.get('username',None)
		password=data.get('password')
		if not email and not username:
			raise ValidationError('A Username or Email is required.')
		user=User.objects.filter(
				Q(email=email) |
				Q(username=username)
			).distinct()
		user=user.exclude(email__isnull=True).exclude(email__iexact='')
		if user.exists() and user.count() == 1:
			user=user.first()
		else:
			raise ValidationError('This username/email is not valid.')
		if user:
			if not user.check_password(password):
				raise ValidationError('Incorrect credentials please try again.')

		return data

class UserCreateSerializer(ModelSerializer):
	email=EmailField(required=True)
	password2=CharField(label='Confirm Password')
	class Meta:
		model=User
		fields=[
			'username',
			'email',
			'password',
			'password2'
		]
		extra_kwargs={
			'password':{"write_only":True}

		}

	def validate(self,data):
		email=data.get("email")
		email_qs=User.objects.filter(email=email)
		username=data.get('username')
		username_qs=User.objects.filter(username=username)
		password=data.get('password')
		password2=data.get('password2')
		if email_qs.exists():
			raise ValidationError('This email has been registered.')
		if username_qs.exists():
			raise ValidationError('This username has been registered.')
		if password != password2:
			raise ValidationError('Password do not match.')
		return data
	def create(self,validated_data):
		username=validated_data.get('username')
		password=validated_data.get('password')
		email=validated_data.get('email')
		user_obj=User(
				username=username,
				email=email,
			)
		user_obj.set_password(password)
		user_obj.save()
		return validated_data