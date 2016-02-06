from django.shortcuts import render
from django.http import JsonResponse
from inventory.models import Floor, Kegerator, Style

# Create your views here.

def index(request):
    floors = Floor.objects.all()
    data = {}
    for floor in floors:
        for keger in floor.kegerator_set.all():
            for keg in keger.keg_set.all():
                if keg.filled and keg.tapped:
                    data[str(floor)] = {}
                    data[str(floor)][str(keger)] = {}
                    data[str(floor)][str(keger)]=str(keg)
    return JsonResponse(data)

def floors(request):
    floors = Floor.objects.all()
    data = {'Floors':[]}
    for floor in floors:
        data['Floors'].append(str(floor))

    return JsonResponse(data)

def floor(request, id):
    floor = Floor.objects.get(id=id)
    data = {id:str(floor)}
    return JsonResponse(data)

def kegerators(request):
    kegers = Kegerator.objects.all()
    data = {'Kegerators':[]}
    for keger in kegers:
        data['Kegerators'].append(str(keger))
    return JsonResponse(data)

def kegerator(request, id):
    keger = Kegerator.objects.get(id=id)
    data = {id:str(keger)}
    return JsonResponse(data)

def styles(request):
    styles = Style.objects.all()
    data = {'styles':[]}
    for style in styles:
        data['styles'].append(str(style))

    return JsonResponse(data)
