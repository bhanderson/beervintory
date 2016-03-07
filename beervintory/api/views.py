from django.shortcuts import render
from django.http import JsonResponse
from inventory.models import Floor, Kegerator, Style, Brewer, Beer

# Create your views here.

def index(request):
    floors = Floor.objects.all()
    data = {}
    for floor in floors:
        for keger in floor.kegerator_set.all():
            for keg in keger.keg_set.all():
                if keg.filled and keg.tapped:
                    if not str(floor) in  data.keys():
                        data[str(floor)] = {}
                    if not str(keger) in data[str(floor)].keys():
                        data[str(floor)][str(keger)] = []
                    data[str(floor)][str(keger)].append(str(keg))
    return JsonResponse(data)

def floors(request):
    floors = Floor.objects.all()
    data = {'Floors':[]}
    for floor in floors:
        data['Floors'].append(str(floor))

    return JsonResponse(data)

def floor(request, id):
    try:
        floor = Floor.objects.get(id=id)
    except:
        return JsonResponse({})
    return JsonResponse({id:str(floor)})

def kegerators(request):
    kegers = Kegerator.objects.all()
    data = {'Kegerators':[]}
    for keger in kegers:
        data['Kegerators'].append(str(keger))
    return JsonResponse(data)

def kegerator(request, id):
    try:
        keger = Kegerator.objects.get(id=id)
    except:
        return JsonResponse({})
    data = {id:str(keger)}
    return JsonResponse(data)

def styles(request):
    styles = Style.objects.all()
    data = {'Styles':[]}
    for style in styles:
        data['Styles'].append(str(style))

    return JsonResponse(data)

def style(request, id):
    try:
        style = Style.objects.get(id=id)
    except:
        return JsonResponse({})
    return JsonResponse({id:str(style)})

def brewers(request):
    brewers = Brewer.objects.all()
    data = {'Brewers':[]}
    for brewer in brewers:
        data['Brewers'].append(str(brewer))
    return JsonResponse(data)

def brewer(request, id):
    try:
        brewer = Brewer.objects.get(id=id)
    except:
        return JsonResponse({})
    return JsonResponse({id:str(brewer)})

def beers(request):
    beers = Beer.objects.all()
    data = {'Beers':[]}
    for beer in beers:
        data['Beers'].append(str(beer))
    return JsonResponse(data)

def beer(request, id):
    try:
        beer = Beer.objects.get(id=id)
    except:
        return JsonResponse({})
    return JsonResponse({id:str(beer)})
