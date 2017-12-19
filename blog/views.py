from django.shortcuts import render

def homeView(request):
	return render(request,'home.html',{})

def contactView(request):
	return render(request,'contact.html',{})
def aboutView(request):
	return render(request,'about.html',{})