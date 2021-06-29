import datetime

from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Employee(models.Model):
    ldap = models.CharField(max_length=50)

    def __str__(self):
        return self.ldap


def get_it_team():
    return Team.objects.get_or_create(name__iexact='it')


def get_it_employee():
    return Employee.objects.get_or_create(ldap__iexact='it')


class Item(models.Model):
    asset_tag = models.IntegerField(primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    specification = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    model = models.CharField(max_length=100)
    service_tag = models.CharField(max_length=100)
    system_name = models.CharField(max_length=100, blank=True, null=True)
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET(get_it_employee), null=True)
    team = models.ForeignKey(Team, on_delete=models.SET(get_it_team), null=True)
    acquisition_date = models.DateField(default=datetime.date.today)
    decommission_date = models.DateField(blank=True, null=True)
    notes = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return str(self.asset_tag)
