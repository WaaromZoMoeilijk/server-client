#from models import Rpi
from django.contrib.auth.models import Rpi
for rpi in Rpi.objects.all():
	print(rpi.id)
