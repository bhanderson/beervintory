from django.shortcuts import render
from inventory.models import Floor
from django.contrib.auth.models import User

def index(request):
    floors = Floor.objects.all()
    logins = []
    for user in User.objects.all():
        logins.append(user.last_login)
    updated = max(logins)
    context = {'Floors': floors, 'Updated': updated}
    return render(request, 'website/index.html', context)

# Create your views here.
