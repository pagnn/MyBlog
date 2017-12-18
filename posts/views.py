from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.http import HttpResponse
# Create your views here.
from .models import Post
from .forms import PostCreateForm
class PostListView(ListView):
	paginate_by=4
	queryset=Post.objects.all()
	def get_context_data(self,*args,**kwargs):
		context=super(PostListView,self).get_context_data(*args,**kwargs)
		print(context)
		return context
	def get(self,request,*args,**kwargs):
		print(request.GET.get('paginator'))
		return super(PostListView,self).get(request,*args,**kwargs)

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
class PostUpdateView(UpdateView):
	model=Post
	fields=['title','content']
	template_name='posts/update.html'

class PostDeleteView(DeleteView):
	model=Post
	success_url=reverse_lazy('posts:list')

