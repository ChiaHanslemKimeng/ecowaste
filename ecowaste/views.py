from django.shortcuts import render, HttpResponseRedirect
from django.db.models import Sum


def login(request):
	user = request.user
	
	return render(request, 'login.html', { })
