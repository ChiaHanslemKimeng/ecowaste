from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views

from .views import *


urlpatterns = [
    path('add_edit_waste_type/<wastetype_id>/', add_edit_waste_type, name='add_edit_waste_type'),

    # path('add_edit_waste_type/<wastetype_id>/', add_edit_waste_type, name='add_edit_waste_type'),

    path('add_waste_availability/', add_waste_availability, name='add_waste_availability'), 
]

