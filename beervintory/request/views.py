from django.shortcuts import render, HttpResponseRedirect
from inventory import models as inv
from request import models
from .forms import RequestForm, NewRequestForm

# Create your views here.
def index(request):
    if request.method == "POST":
        if 'new_request' in request.POST:
            new = models.Request()
            new.beer = request.POST['new_request']
            new.number = 0
            new.save()
        elif 'request' in request.POST.keys():
            req = models.Request.objects.filter(
                    beer=request.POST['request'])[0]
            req.number+=1
            req.save()
        return HttpResponseRedirect('request')
    else:
        form = RequestForm()
        newform = NewRequestForm()
    return render(request, 'request/index.html',
            {'form': form, 'newform': newform,
        'Requests':models.Request.objects.all()})


"""
        newform = NewRequestForm(request.POST)
        form = RequestForm(request.POST)
        if newform.is_valid:
            print request.POST
            if request.POST.has_key('new_request') and request.POST['new_request']:
                new = models.Request()
                new.beer = request.POST['new_request'][0]
                new.number = 0
                new.save()
            else:
                return HttpResponseRedirect('request')
        if form.is_valid:
            # if we have a valid answer, ie. not new
            if request.POST.has_key('request') and request.POST['request']:
                req = models.Request.objects.filter(
                        beer=request.POST['request'])[0]
                req.number+=1
                req.save()
            else:
                return HttpResponseRedirect('request')
    else:
        form = RequestForm()
        newform = NewRequestForm()
    return render(request, 'request/index.html',
            {'form': form, 'newform': newform,
        'Requests':models.Request.objects.all()})
        """
