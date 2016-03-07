from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from request import models
from .forms import RequestForm, NewRequestForm
import json

# Create your views here.
def index(request):
    ip = request.META.get('REMOTE_ADDR')
    if request.method == "POST":
        if 'new_request' in request.POST:
            req = models.Request()
            req.beer = request.POST['new_request']
            req.number = 1
            req.requesters = json.dumps([ip])
            try:
                req.save()
            except IntegrityError:
                return HttpResponse("Sorry that request already exists")
        elif 'request' in request.POST.keys():
            req = models.Request.objects.get(id=request.POST['request'])
            if req:
                jd = json.decoder.JSONDecoder()
                l = jd.decode(req.requesters)
                if ip in l:
                    return HttpResponse("Sorry your IP already voted for this request")
                req.number+=1
                reqer = models.Requester()
                reqer.request = req
                reqer.ip = ip
                req.save()
                reqer.save()
        return HttpResponseRedirect('request')
    form = RequestForm()
    newform = NewRequestForm()
    return render(request, 'request/index.html',
            {'form': form, 'newform': newform,
                'Requests':models.Request.objects.all()})
