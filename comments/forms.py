from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
	content=forms.CharField(widget=forms.TextInput,label='Comment')
	email=forms.EmailField(widget=forms.TextInput)
	class Meta:
		model=Comment
		fields=['content','email']