# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

# Extends AbstractUser.
# Fields in AbstractUser:
class CustomUser(AbstractUser):
    # add additional fields in here\
    email = models.EmailField(('email address'), unique=True)
    college = models.CharField(default='humboldt.edu', max_length=200, null=True)
    MY_GENDER_CHOICES = (
        ('U', 'Undeclared'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Nonbinary')
    )
    gender = models.CharField(max_length=1, choices=MY_GENDER_CHOICES, null=True)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=200, null=True)
    verification_date = models.DateTimeField('date verified', null=True)
    has_accepted_tos = models.BooleanField(default=False)
    
    def __str__(self):
        #return '{} ({})'.format(self.username, self.email)
        return '{}'.format(self.id)