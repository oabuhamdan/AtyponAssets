# Create your views here.
from django.shortcuts import render

from Inventory.models import Item


def home_page(request):
    items = Item.objects.all()
    data = {"items": items}
    return render(request, "details.html", data)
