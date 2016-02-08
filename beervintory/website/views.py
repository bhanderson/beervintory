from django.shortcuts import render
from inventory.models import Floor

def index(request):
    floors = Floor.objects.all()
    context = {'Floors': floors}
    return render(request, 'website/index.html', context)

# Create your views here.
