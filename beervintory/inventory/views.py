from django.shortcuts import render
from models import Beer

# Create your views here.
def index(request):
    beers = Beer.objects.all()
    context = {'Beers':beers}
    return render(request, 'inventory/index.html', context)
