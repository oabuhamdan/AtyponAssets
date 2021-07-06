from django.conf.urls import url
from django.contrib.auth.decorators import user_passes_test
from django.urls import path

from Inventory import views

urlpatterns = [
    path('', views.home_page),
    path('upload/', views.upload_file),
    path('edit/', views.edit_row),
    url('add_item/', user_passes_test(lambda u: u.is_active and u.is_staff)(views.AddItem.as_view()), name="add_item"),
]
