from django.db import models

# Create your models here.

class Appointment(models.Model):
    """ Appointment table """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    date = models.DateField()
    department = models.CharField(max_length=10)
    doctor = models.CharField(max_length=10)
    message = models.TextField()
    
    # To return the values in human readable format

    def __str__(self):
        return self.name