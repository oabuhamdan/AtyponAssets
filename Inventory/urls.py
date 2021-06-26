from django.urls import path

from Inventory import views

urlpatterns = [
    path('', views.home_page),
]
