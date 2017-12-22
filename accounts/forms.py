from django import forms
from django.contrib.auth import authenticate,get_user_model,login,logout

User=get_user_model()

class UserLoginForm(forms.Form):
	username=forms.CharField()
	password=forms.CharField(widget=forms.PasswordInput)

	def clean(self,*args,**kwargs):
		username=self.cleaned_data.get('username')
		password=self.cleaned_data.get('password')
		if username and password:
			user=authenticate(username=username,password=password)

			if not user:
				raise forms.ValidationError('This user does not exist.')
			if not user.check_password(password):
				raise forms.ValidationError('Incorrect Password')
			if not user.is_active:
				raise forms.ValidationError('This user is not active')
		return super(UserLoginForm,self).clean(*args,**kwargs)
class UserRegisterForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput,label='Password')
	password2=forms.CharField(widget=forms.PasswordInput,label='Confirm Password')
	class Meta:
		model=User
		fields=[
			'username',
			'email',
			'password'
		]
	def clean_password2(self):
		password=self.cleaned_data.get('password')
		password2=self.cleaned_data.get('password2')
		if password2 != password:
			raise forms.ValidationError('Password must match')
		return password2

	def clean_email(self):
		email=self.cleaned_data.get('email')
		qs=User.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError('This email has been registered.')
		return email
