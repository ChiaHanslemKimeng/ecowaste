from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class User(AbstractUser):
	GENDER = (
		(u'M', u'Male'),
		(u'F', u'Female'),
	)

	MARITAL_STATUS = (
		(u'S', u'Single'),
		(u'M', u'Married'),
		(u'D', u'Divorced'),
		(u'W', u'Widowed'),
	)

	LANGUAGE = (
		(u'en', u'English'),
		(u'fr', u'French'),
	)

	uid					= models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
	gender              = models.CharField(max_length=20, choices=GENDER, null=True)
	marital_status      = models.CharField(max_length=10, choices=MARITAL_STATUS, null=True)
	date_of_birth       = models.DateField(null=True)
	place_of_birth      = models.CharField(max_length=200, null=True)
	nationality         = models.CharField(max_length=200, null=True)
	nic_num             = models.CharField(max_length=100, null=True)
	address             = models.TextField(null=True)
	phone1              = models.CharField(max_length=100, null=True)
	passport_photo      = models.ImageField(upload_to='users_photo', null=True)
	prefered_language   = models.CharField(max_length=20, choices=LANGUAGE, default='en')

	# Flags
	is_standard         = models.BooleanField(default=False)
	is_admin	        = models.BooleanField(default=False)
	is_staff_member     = models.BooleanField(default=False)

	# Password Recovery
	security_question       = models.CharField(blank=True, null=True, max_length=200)
	security_question_slug  = models.SlugField(blank=True, null=True, max_length=200)
	security_answer         = models.CharField(blank=True, null=True, max_length=200)
	security_answer_slug    = models.SlugField(blank=True, null=True, max_length=200)

	# Activity & Metadata
	created_by              = models.ForeignKey('self', related_name='user_created_by', null=True, editable=False, on_delete=models.SET_NULL)
	modified_by             = models.ForeignKey('self', related_name='user_modified_by', null=True, editable=False, on_delete=models.SET_NULL)
	auto_date_created       = models.DateTimeField(auto_now_add=True, null=True)
	auto_date_time_updated  = models.DateTimeField(auto_now=True, null=True)
	auto_date_only          = models.DateField(auto_now_add=True, null=True)
	last_login_date         = models.DateField(auto_now_add=True, null=True)


	class Meta:
		ordering = ['-date_joined']

	@property
	def get_full_name(self):
		return f"{self.first_name} {self.last_name}"