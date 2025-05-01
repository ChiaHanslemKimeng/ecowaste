from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseRedirect,HttpResponseForbidden
from django.template.defaultfilters import slugify
from django.db import transaction
from django.db.models import Q, Avg, Sum

from .models import *
from users.models import User
import datetime

# Create your views here.

@transaction.atomic
@login_required(login_url='/users/login/')
def add_edit_waste_type(request, wastetype_id):
	user = request.user
	get_wastetype = None
	try:
		get_wastetype = WasteType.objects.get(id=wastetype_id)
	except:
		pass

	creating = get_wastetype is None

	if request.POST:
		print(request.POST)
		name = request.POST['name']
		short_name = request.POST['description']
		if not name:
			content_msg = {'status': 'error', 'msg': "Waste Name required", 'redirect_url': ''}
			return JsonResponse(content_msg, content_type='application/json')

		name_query = WasteType.objects.filter(name= name)
		if not creating:
			name_query = name_query.exclude(id = get_wastetype.id)

		if name_query.exists():
			content_msg = {'status': 'error', 'msg': "Waste Name already exist", 'redirect_url': ''}
			return JsonResponse(content_msg, content_type='application/json')

		if creating:
			get_wastetype = WasteType()  # Initialize a new WasteType object
		else:
			get_wastetype = get_wastetype  # Use the existing WasteType for editing

		get_wastetype.name = request.POST['name'].upper()
		get_wastetype.description = request.POST['description']
		get_wastetype.save()

		content_msg = {'status': 'ok', 'msg': "Successful", 'redirect_url': '/setup/institutions/', 'timer':5000}
		return JsonResponse(content_msg, content_type='application/json')

	else:
		if get_wastetype:
			get_institution_id = get_wastetype.id
			page_title = _("Edit Waste")
		else:
			get_institution_id = 'new'
			page_title = _("Register Waste Type")

		return render(request, 'setup/add_edit_waste_type.html', {'creating':creating, 'get_wastetype':get_wastetype,  'page_title':page_title, 'get_institution_id':get_institution_id})


@transaction.atomic
@login_required(login_url='/users/login/')
def add_waste_availability(request):
	user = request.user
	if request.POST:
		get_wastetype = request.POST['waste_type']
		location = request.POST['location']
		if not get_wastetype:
			error_msg = "Wast type is required"
			return render(request, 'add_waste_availability.html', {'error_msg':error_msg})
		if location == '':
			error_msg = "Location is required"
			return render(request, 'add_waste_availability.html', {'error_msg':error_msg})
			
		new_waste = WasteAvailabilityNotification()
		new_waste.user = user
		new_waste.waste_type = WasteType.objects.get(id = get_wastetype)
		new_waste.location = location
		new_waste.description = request.POST['description']
		new_waste.save()

		return HttpResponseRedirect('/users/home/')
	else:
		return render(request, 'add_waste_availability.html', {})
	