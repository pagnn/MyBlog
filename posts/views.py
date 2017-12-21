from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .models import Post
from .forms import PostCreateForm
class PostListView(ListView):
	paginate_by=4
	queryset=Post.objects.all()
	def get_context_data(self,*args,**kwargs):
		context=super(PostListView,self).get_context_data(*args,**kwargs)
		return context
	def get(self,request,*args,**kwargs):
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
class PostCreateView(LoginRequiredMixin,CreateView):
	form_class=PostCreateForm
	template_name='posts/create.html'
	def post(self,request,*args,**kwargs):
		if request.method == 'POST':
			print(request.FILES)
			form = PostCreateForm(request.POST or None, request.FILES or None)
			if form.is_valid():
				instance=form.save(commit=False)
				instance.user=request.user
				instance.save()
				return HttpResponseRedirect(instance.get_absolute_url())
		else:
			form = PostCreateForm()
		return render(request, 'posts/create.html', {'form': form})
class PostUpdateView(LoginRequiredMixin,UpdateView):
	model=Post
	form_class=PostCreateForm
	template_name='posts/update.html'

class PostDeleteView(LoginRequiredMixin,DeleteView):
	model=Post
	success_url=reverse_lazy('posts:list')

