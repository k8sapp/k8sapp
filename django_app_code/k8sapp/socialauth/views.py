from django.shortcuts import render

# Create your views here.
def landing(request):
	print('in socialauth landing views.py')
	return render(request,'socialauth/landing.html')

def login(request):
	print('in socialauth login views.py')
	return render(request,'socialauth/login.html')
