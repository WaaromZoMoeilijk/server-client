from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	request.session = {'userid': ''}
	return render(request, 'login.html')
