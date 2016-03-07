from django.shortcuts import render
from models import Rate, Beer

# Create your views here.
def index(request):
    context = {'Ratings':[]}
    for beer in Beer.objects.all():
        selection = Rate.objects.filter(beer=beer)
        rates = []
        for select in selection:
            rates.append(select.rating)
            context['Ratings'].append((str(select.beer),
                sum(rates) / float(len(rates))))
    return render(request, 'rate/index.html', context)
