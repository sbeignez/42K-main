from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from app.models import RaceEvent

def home(request):
    return render(request, 'app/home.html')

class RunnerView(generic.ListView):
    template_name = 'app/runner.html'
    context_object_name = 'races'

    def get_queryset(self):
        return RaceEvent.objects.all()

class TaggerView(generic.ListView):
    template_name = 'app/tagger.html'
    context_object_name = 'races'

    def get_queryset(self):
        return RaceEvent.objects.all()

def photographer(request):
    return render(request, 'app/photographer.html')
