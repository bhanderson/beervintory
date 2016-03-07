from django.db import IntegrityError
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .forms import RateForm, BeerForm
from models import Rate, Beer
import json

# Create your views here.
def new_rating(beer, rating, ip):
    new_rate = Rate()
    new_rate.beer = beer
    new_rate.rating = rating
    new_rate.raters = json.dumps({ip:rating})
    new_rate.save()
    return HttpResponseRedirect('rate')

def add_rating(beer, rating, ip):
    try:
        rate = Rate.objects.get(beer=beer)
    except ValueError:
        return HttpResponse("could not find rating")
        return HttpResponseRedirect('rate')
    jd = json.decoder.JSONDecoder()
    d = jd.decode(rate.raters)
    if ip in d.keys():
        return HttpResponse("Sorry your IP {0} already rated this beer".format(ip))
    d[ip] = rating
    total = 0
    for i,v in d.iteritems():
        total += int(v)
    avg = total/len(d)
    rate.rating = avg
    rate.raters = json.dumps(d)
    rate.save()
    return HttpResponseRedirect('rate')

def index(request):
    ip = request.META.get('REMOTE_ADDR')
    if request.method == "POST":
        if ('beer' in request.POST and 'rating' in request.POST):
            beer = None
            rating = None
            try:
                beer = Beer.objects.get(id=request.POST['beer'])
                rating = int(request.POST['rating'])
                if (not rating) or (rating <= 0) or (rating >= 100):
                    raise ValueError
            except ValueError:
                return HttpResponse("Sorry your rating was not within 100")
            # so we have both a beer and rating now
            # check if we have any ratings already for this beer
            # if we dont make a new one
            try:
                return new_rating(beer, rating, ip)
            except IntegrityError:
                return add_rating(beer, rating, ip)
    beer = BeerForm()
    rate = RateForm()
    return render(request, 'rate/index.html',
            {'beer': beer, 'rate': rate,
                'Ratings': Rate.objects.all()})
