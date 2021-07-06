from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Inventory.helper import add_items_to_db, get_dropdown_items, update_row
from Inventory.models import *


@login_required
def home_page(request):
    items = Item.objects.all()
    dropdown_items = get_dropdown_items()
    data = {"items": items, 'dropdown_items': dropdown_items}
    return render(request, "details.html", data)


@staff_member_required
def upload_file(request):
    if request.method == 'GET':
        return render(request, "upload_file.html")
    else:
        add_items_to_db(request)
        return redirect('/')


@staff_member_required
def edit_row(request):
    return update_row(request)


class AddItem(CreateView):
    model = Item
    template_name = 'addItem.html'
    fields = ['asset_tag', 'location', 'specification', 'brand', 'model', 'service_tag', 'system_name', 'assigned_to',
              'team', 'acquisition_date', 'decommission_date', 'notes']
    success_url = "/"
