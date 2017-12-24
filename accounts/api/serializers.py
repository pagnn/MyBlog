from rest_framework.serializers import EmailField,CharField,ModelSerializer,HyperlinkedIdentityField,SerializerMethodField,ValidationError


from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User=get_user_model()

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
		password=data.get('password')
		password2=data.get('password2')
		if email_qs.exists():
			raise ValidationError('This email has been registered.')
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