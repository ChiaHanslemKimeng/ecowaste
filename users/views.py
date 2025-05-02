from django.shortcuts import render
from django.contrib.auth.models import User, Group, Permission
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout  as django_logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.template.loader import render_to_string
import re

from .models import *
# Create your views here.

def validate_email(email):
	if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
		return True
	else:
		return False



def login_user(request):
	user = request.user
	print("==== In the login ===")

	if request.POST:
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username = username, password = password)

		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/users/home/')
		else:
			error_msg = "invalid Username or Password"
			return render(request, 'login.html', {'user': user, 'error_msg':error_msg})
	else:
		return render(request, 'users/login.html', {'user':user})

@login_required
def home(request):
	return render(request, 'index.html', {})


@login_required
def logout(request):
	django_logout(request)
	return HttpResponseRedirect('/')



@transaction.atomic
def register_user(request):
	user = request.user
	
	if request.POST:
		print(request.POST)

		first_name = ' '.join(request.POST['first_name'].strip().split())
		last_name = ' '.join(request.POST['last_name'].strip().split())
		email = request.POST['email']
		phone_number = request.POST['phone']
		username = email
		if not validate_email(email):
			error_msg = "Invalid email address"
			return render(request, 'users/register_user.html', {'error_msg': error_msg, })
		password1 = request.POST['password']
		password2 = request.POST['password2']

		if password1 != password2:
			error_msg = "Passwords does not match"
			return render(request, 'users/register_user.html', {'error_msg': error_msg, })
		
		max_pass_length = 8
		if len(password1) < max_pass_length:
			error_msg = "Password must be at least 8 characters"
			return render(request, 'users/register_user.html', {'error_msg': error_msg, })

		check_username = None
		try:
			check_username = User.objects.get(username__iexact=username)
		except:
			pass
		if check_username:
			error_msg = "Email already taken!"
			return render(request, 'users/register_user.html', {'error_msg': error_msg, })


		"""create user"""
		new_user =  User()
		new_user.username = username
		new_user.set_password(password1)
		new_user.email = email
		new_user.is_staff = False
		new_user.is_active = True
		new_user.first_name = first_name
		new_user.last_name = last_name
		new_user.phone1 = phone_number
		new_user.save()

		login(request, new_user)

		return HttpResponseRedirect("/users/home/")

	else:
		return render(request, 'users/register_user.html', {})
	

def messages(request):
	user = request.user
 
	return render(request, 'users/messages.html', {})




def users(request):
	user = request.user
 
	return render(request, 'users/users.html', {})