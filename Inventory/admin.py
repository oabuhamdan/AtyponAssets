from django.contrib import admin


# Register your models here.
from Inventory.models import *

admin.site.register(Item)
admin.site.register(Team)
admin.site.register(Employee)
admin.site.register(Brand)
admin.site.register(Location)
