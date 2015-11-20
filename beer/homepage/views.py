from django.shortcuts import render
from inventory.models import Floor

# Create your views here.

def index(request):
    floors = Floor.objects.all()
    context = {'Floors': floors}
    return render(request, 'homepage/index.html', context)
