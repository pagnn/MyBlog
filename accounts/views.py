from django.shortcuts import render
from django.contrib.auth import authenticate,get_user_model,login,logout
# Create your views here.
from .forms import UserLoginForm,UserRegisterForm


def login_view(request):
	form=UserLoginForm(request.POST or None)
	if form.is_valid():
		username=form.cleaned_data.get('username')
		password=form.cleaned_data.get('password')
		user=authenticate(username=username,password=password)
		login(request,user)
	context={
		'form':form,
	}

	return render(request,'accounts/login.html',context)

def logout_view(request):
	logout(request)
	return render(request,'accounts/logout.html',{})


def register_view(request):
	form=UserRegisterForm(request.POST or None)
	if form.is_valid():
		instance=form.save(commit=False)
		username=form.cleaned_data.get('username')
		password=form.cleaned_data.get('password')
		instance.set_password(password)
		instance.save()
		user=authenticate(username=username,password=password)
		login(request,instance)
	context={
		'form':form
	}
	return render(request,'accounts/register.html',context)
