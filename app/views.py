from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'app/home.html')

def runner(request):
    return render(request, 'app/runner.html')

def tagger(request):
    return render(request, 'app/tagger.html')

def photographer(request):
    return HttpResponse("TODO")