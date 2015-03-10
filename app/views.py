from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'app/home.html')

def runner(request):
    return render(request, 'app/runner.html')

def photographer(request):
    return HttpResponse("TODO")