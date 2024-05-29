from django.contrib import admin
from .models import Facility,Booking
from .customer import Customer

# Register your models here.
admin.site.register(Facility)
admin.site.register(Booking)
admin.site.register(Customer)