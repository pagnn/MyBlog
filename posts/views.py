from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView
from django.http import HttpResponse
# Create your views here.
from .models import Post
from .forms import PostCreateForm
class PostListView(ListView):
	queryset=Post.objects.all()
	def get_context_data(self,*args,**kwargs):
		context=super(PostListView,self).get_context_data(*args,**kwargs)
		print(context)
		return context

class PostDetailView(DetailView):
	template_name='posts/post_detail.html'
	def get_object(self,*args,**kwargs):
		request=self.request
		slug=self.kwargs.get('slug')
		qs=Post.objects.filter(slug=slug)
		if qs.exists():
			return qs.first()
		return HttpResponse('Post not found.')
class PostCreateView(CreateView):
	form_class=PostCreateForm
	template_name='posts/create.html'



