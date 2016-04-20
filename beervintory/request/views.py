from django.db import IntegrityError
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .forms import RequestForm, NewRequestForm
from request import models
import json

# Create your views here.
def index(request):
    ip = request.META.get('HTTP_X_REAL_IP')
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
            req = None
            l = []
            try:
                req = models.Request.objects.get(id=request.POST['request'])
            except ValueError:
                return HttpResponseRedirect('')
            # if we have the request start the addition
            if req:
                jd = json.decoder.JSONDecoder()
                l = jd.decode(req.requesters)
                if ip in l:
                    return HttpResponse("Sorry your IP ({0}) already voted for this request".format(ip))
                req.number+=1
                l.append(ip)
                req.requesters = json.dumps(l)
                try:
                    req.save()
                except IntegrityError:
                    return HttpResponse("Error")
        # if we get a different post
        return HttpResponseRedirect('')
    # if we are displaying the website create the forms and send the requests
    form = RequestForm()
    newform = NewRequestForm()
    return render(request, 'request/index.html',
            {'form': form, 'newform': newform,
                'Requests':models.Request.objects.all().order_by('-number')})
