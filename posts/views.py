from django.shortcuts import render
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
# Create your views here.
from .models import Post
from .forms import PostCreateForm
from comments.models import Comment	
from comments.forms import CommentForm
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
	def get_success_url(self):
		return reverse('posts', kwargs={'slug': self.slug})
	def get_object(self,*args,**kwargs):
		request=self.request
		slug=self.kwargs.get('slug')
		qs=Post.objects.filter(slug=slug)
		if qs.exists():
			return qs.first()
		return HttpResponse('Post not found.')
	def get_context_data(self,*args,**kwargs):
		context=super(PostDetailView,self).get_context_data(*args,**kwargs)
		instance=context['object']		
		comments=Comment.objects.filter_by_instance(instance)
		context['comments']=comments		

		commentForm=CommentForm()
		context['commentForm']=commentForm
		return context
	def post(self,request,*args,**kwargs):
		obj=self.get_object()
		if request.method == 'POST':
			form=CommentForm(request.POST or None,initial={
				'content_type':obj.get_content_type,
				'object_id':obj.id
			})
			if form.is_valid():
				instance=form.save(commit=False)
				return HttpResponseRedirect(obj.get_absolute_url())
			else:
				form=CommentForm()
		return HttpResponseRedirect(reverse('posts:detail', kwargs={'slug': obj.slug}))


class PostCreateView(LoginRequiredMixin,CreateView):
	form_class=PostCreateForm
	template_name='posts/create.html'
	def post(self,request,*args,**kwargs):
		if request.method == 'POST':
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

