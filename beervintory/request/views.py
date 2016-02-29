from django.shortcuts import render, HttpResponseRedirect
from inventory import models as inv
from request import models
from .forms import RequestForm

# Create your views here.
def index(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid:
            # if we have a valid answer, ie. not new
            if request.POST['request']:
                req = models.Request.objects.filter(
                        beer_id=request.POST['request'])[0]
                req.number+=1
                req.save()
            else:
                return HttpResponseRedirect('request')
    else:
        form = RequestForm()
    return render(request, 'request/index.html', {'form': form,
        'Requests':models.Request.objects.all()})
