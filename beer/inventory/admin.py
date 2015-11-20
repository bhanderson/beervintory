from django.contrib import admin

# Register your models here.
from .models import Floor, Kegerator, Keg, Style, Brewer, Beer

admin.site.register(Floor)
admin.site.register(Kegerator)
admin.site.register(Keg)
admin.site.register(Style)
admin.site.register(Brewer)
admin.site.register(Beer)
