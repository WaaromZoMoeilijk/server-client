from django.contrib import admin

#from .models import Xuser
from xx.models import Xuser, CliCommand, NewNetwork, Rpi, RpiLogline, RpiCliCommand, NewRpi, Settings

# Register your models here.
admin.site.register(Xuser)
admin.site.register(CliCommand)
admin.site.register(NewNetwork)
admin.site.register(NewRpi)
admin.site.register(Rpi)
admin.site.register(RpiLogline)
admin.site.register(RpiCliCommand)
admin.site.register(Settings)
