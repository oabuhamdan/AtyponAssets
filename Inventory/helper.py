import dateutil.parser
import pandas as pd
from django.contrib import messages

from Inventory.models import *


def fix_foreign_keys(request):
    attrib_dict = request.POST.dict()
    attrib_dict.pop('csrfmiddlewaretoken')
    attrib_dict.pop('action')
    attrib_dict['location'] = Location.objects.filter(name__iexact=attrib_dict['location']).first()
    attrib_dict['brand'] = Brand.objects.filter(name__iexact=attrib_dict['brand']).first()
    attrib_dict['assigned_to'] = Employee.objects.filter(name__iexact=attrib_dict['assigned_to']).first()
    attrib_dict['team'] = Team.objects.filter(name__iexact=attrib_dict['team']).first()
    attrib_dict['acquisition_date'] = dateutil.parser.parse(attrib_dict['acquisition_date']) if attrib_dict[
                                                                                                    'acquisition_date'] is not '' else None
    attrib_dict['decommission_date'] = dateutil.parser.parse(attrib_dict['decommission_date']) if attrib_dict[
                                                                                                      'decommission_date'] is not '' else None

    return attrib_dict


def update_row(request):
    try:
        attrib_dict = fix_foreign_keys(request)
        asset_tag = attrib_dict.pop('asset_tag')
        Item.objects.filter(asset_tag=asset_tag).update(**attrib_dict)
    except Exception as e:
        print(e)
        return False
    return True


def objects_to_json_string(objects):
    json_list = []
    for obj in objects.iterator():
        json_list.append('"{}":"{}"'.format(obj.name, obj.name))

    return "{" + ",".join(json_list) + "}"


def get_dropdown_items():
    data = {
        "locations": objects_to_json_string(Location.objects.all()),
        "brands": objects_to_json_string(Brand.objects.all()),
        "teams": objects_to_json_string(Team.objects.all()),
        "employees": objects_to_json_string(Employee.objects.all()),
    }
    return data


def add_items_to_db(request):
    file_path = request.FILES['file_path']
    df = pd.read_csv(file_path.temporary_file_path(), na_filter=False)
    items = [row for index, row in df.iterrows()]
    failed_to_add_assets_tags = []
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
            failed_to_add_assets_tags.append(str(item[0]))
            print('Failed to add asset with tag: ' + str(item[0]), e)

    if len(failed_to_add_assets_tags) > 0:
        messages.warning(request, 'Failed to add these asset tags\n' + ', '.join(failed_to_add_assets_tags))
