from django.db import models

class Facility(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    image = models.ImageField(upload_to='facility_images/')

    def __str__(self):
        return self.name

class Booking(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f'{self.facility.name} from {self.start_time} to {self.end_time}'
