from django.contrib import admin

# Register your models here.
from .models import Floor, Kegerator, Keg, Style, Brewer, Beer

class KegeratorInline(admin.TabularInline):
    model = Kegerator
    extra = 0
    show_change_link = True

class KegInline(admin.TabularInline):
    model = Keg
    extra = 0
    show_change_link = True

class FloorAdmin(admin.ModelAdmin):
    inlines = [
            KegeratorInline,
    ]

class KegeratorAdmin(admin.ModelAdmin):
    inlines = [
            KegInline,
    ]

admin.site.register(Floor, FloorAdmin)
admin.site.register(Kegerator, KegeratorAdmin)
admin.site.register(Keg)
admin.site.register(Style)
admin.site.register(Brewer)
admin.site.register(Beer)
