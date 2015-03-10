from django.shortcuts import render

def home(request):
    return render(request, 'app/home.html')

def runner_login(request):
    return render(request, 'app/login-runner.html')