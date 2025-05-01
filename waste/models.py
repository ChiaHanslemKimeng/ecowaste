from django.db import models

from users.models import User  # Import Django's built-in User model
from django.core.validators import MinValueValidator
# Create your models here.


class WasteType(models.Model):
	"""Represents a type of waste (e.g., Recyclable, Organic, Hazardous)."""
	name = models.CharField(max_length=50, unique=True)
	description = models.TextField(blank=True, null=True)

	#auto (this fields below will be updated automatically)
	created_by = models.ForeignKey(User, related_name = 'WasteType_created_by', null = True, editable=False, on_delete=models.CASCADE)
	modified_by = models.ForeignKey(User, related_name = 'WasteType_modified_by', null = True, editable=False, on_delete=models.CASCADE)
	auto_date_created = models.DateTimeField(auto_now_add=True, null = True)
	auto_date_time_updated = models.DateTimeField(auto_now = True, null = True)
	auto_date_only = models.DateField(auto_now_add = True, null = True)

	def __str__(self):
		return self.name

class WasteAvailabilityNotification(models.Model):
	"""Represents a notification from a resident about waste availability."""
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='waste_notifications')
	waste_type = models.ForeignKey(WasteType, on_delete=models.PROTECT)
	quantity = models.PositiveIntegerField(default=1) # Number of bags, containers, etc.
	location = models.CharField(max_length=50, null = True)
	description = models.TextField(blank=True, null=True)
	notification_date = models.DateTimeField(auto_now_add=True)
	is_collected = models.BooleanField(default=False)

	#auto (this fields below will be updated automatically)
	created_by = models.ForeignKey(User, related_name = 'WasteAvailabilityNotification_created_by', null = True, editable=False, on_delete=models.CASCADE)
	modified_by = models.ForeignKey(User, related_name = 'WasteAvailabilityNotification_modified_by', null = True, editable=False, on_delete=models.CASCADE)
	auto_date_created = models.DateTimeField(auto_now_add=True, null = True)
	auto_date_time_updated = models.DateTimeField(auto_now = True, null = True)
	auto_date_only = models.DateField(auto_now_add = True, null = True)

	def __str__(self):
		return f"{self.user.username} - {self.waste_type.name} - {self.notification_date}"


class WasteCollectionRequest(models.Model):
	"""Represents a request from a resident to schedule a waste collection."""
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collection_requests')
	request_date = models.DateTimeField(auto_now_add=True)
	# collection_schedule = models.ForeignKey(CollectionSchedule, on_delete=models.PROTECT)
	notes = models.TextField(blank=True, null=True)
	is_confirmed = models.BooleanField(default=False)  # Has the request been confirmed?

	#auto (this fields below will be updated automatically)
	created_by = models.ForeignKey(User, related_name = 'WasteCollectionRequest_created_by', null = True, editable=False, on_delete=models.CASCADE)
	modified_by = models.ForeignKey(User, related_name = 'WasteCollectionRequest_modified_by', null = True, editable=False, on_delete=models.CASCADE)
	auto_date_created = models.DateTimeField(auto_now_add=True, null = True)
	auto_date_time_updated = models.DateTimeField(auto_now = True, null = True)
	auto_date_only = models.DateField(auto_now_add = True, null = True)

	def __str__(self):
		return f"{self.user.username} - {self.collection_schedule} - {self.request_date}"


class CollectionSchedule(models.Model):
	"""Represents a scheduled waste collection."""
	date = models.DateField()
	time = models.TimeField()
	route_name = models.CharField(max_length=100)  # e.g., "Route A - Monday"
	waste = models.ManyToManyField(WasteCollectionRequest, related_name='collections')
	# Add a ForeignKey to a location model if you have one
	# location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return f"{self.route_name} - {self.date}"





class CollectionRoute(models.Model):
	"""Represents a waste collection route."""
	name = models.CharField(max_length=100, unique=True)
	schedule = models.ForeignKey(CollectionSchedule, on_delete=models.PROTECT)
	# vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
	collector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'groups__name': 'Waste Collectors'})  # Only allow users in the "Waste Collectors" group
	route_details = models.TextField(blank=True, null=True) # Description of the route

	def __str__(self):
		return self.name

class CollectionStatusUpdate(models.Model):
	"""Represents an update on the status of a waste collection."""
	collection_route = models.ForeignKey(CollectionRoute, on_delete=models.CASCADE, related_name='status_updates')
	timestamp = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=50)  # e.g., "En Route", "Collecting", "Completed", "Delayed"
	notes = models.TextField(blank=True, null=True)

	def __str__(self):
		return f"{self.collection_route.name} - {self.timestamp} - {self.status}"


class DisposalReport(models.Model):
	"""Represents a report on waste processing and disposal."""
	report_date = models.DateField()
	waste_type = models.ForeignKey(WasteType, on_delete=models.PROTECT)
	quantity_processed = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
	disposal_method = models.CharField(max_length=100)  # e.g., "Landfill", "Incineration", "Recycling"
	notes = models.TextField(blank=True, null=True)

	def __str__(self):
		return f"{self.facility.name} - {self.report_date} - {self.waste_type.name}"