import dateutil.parser
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Inventory.models import *


@login_required
def home_page(request):
    items = Item.objects.all()
    data = {"items": items}
    return render(request, "details.html", data)


@login_required
def upload_file(request):
    if request.method == 'GET':
        return render(request, "upload_file.html")
    else:
        add_items_to_db(request)
        return redirect('/')


def add_items_to_db(request):
    file_path = request.FILES['file_path']
    df = pd.read_csv(file_path.temporary_file_path(), na_filter=False)
    items = [row for index, row in df.iterrows()]
    for item in items:
        try:
            location = Location.objects.get_or_create(name=item[1].upper())[0]
            brand = Brand.objects.get_or_create(name=item[3])[0]
            assigned_to = Employee.objects.get_or_create(ldap=item[7].lower())[0]
            team = Team.objects.get_or_create(name=item[8].upper())[0]
            acq_date = dateutil.parser.parse(item[9]) if item[9] is not '' else None
            dec_date = dateutil.parser.parse(item[10]) if item[10] is not '' else None
            Item.objects.create(asset_tag=item[0], location=location, specification=item[2], brand=brand,
                                model=item[4], service_tag=item[5], system_name=item[6], assigned_to=assigned_to,
                                team=team,
                                acquisition_date=acq_date, decommission_date=dec_date, notes=item[11])
        except Exception as e:
            print(e)
