from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Comment
from .forms import CommentForm
# Create your views here.



def comment_thread(request,pk):
	obj=get_object_or_404(Comment,pk=pk)
	form=CommentForm(request.POST or None)
	parent_obj=None
	try:
		parent_id=request.POST.get('parent-id')
	except:
		parent_id=None
	if parent_id:
		parent_qs=Comment.objects.filter(id=parent_id)
		if parent_qs.exists():
			parent_obj=parent_qs.first()
	if request.method == 'POST':		
		if form.is_valid():
			cd=form.cleaned_data
			content=cd.get('content')
			email=cd.get('email')
			new_c,created=Comment.objects.get_or_create(
					post=parent_obj.post,
					content=content,
					email=email,
					parent=parent_obj,
				)
			return HttpResponseRedirect(obj.get_absolute_url())
		else:

			form=CommentForm()
	context={
		'comment':obj,
		'commentForm':form,
	}
	return render(request,'comments\comment_thread.html',context)