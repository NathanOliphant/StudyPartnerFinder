# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

MY_GENDER_CHOICES = (
    ('U', 'Undeclared'),
    ('M', 'Male'),
    ('F', 'Female'),
    ('N', 'Nonbinary')
)
#
#    The default user model for Django does not include some fields we need.
#    So, we are extending it here and using it in place of the default user.


# Extends AbstractUser.
# Fields in AbstractUser:
class CustomUser(AbstractUser):
    # add additional fields in here\
    email = models.EmailField(('email address'), unique = True)
    # For now, our college will always be humboldt.edu.  When new colleges added,
    # this, and the email functionality, will need to be udpated.
    college = models.CharField(default = 'humboldt.edu', max_length = 200, null = True)
    gender = models.CharField(max_length = 1, choices = MY_GENDER_CHOICES, null = True)
    is_verified = models.BooleanField(default = False)
    verification_code = models.CharField(max_length = 200, null = True)
    verification_date = models.DateTimeField('date verified', null = True)
    has_accepted_tos = models.BooleanField(default = False)

    # def __str__(self):
    #    return '{}'.format(self.id)
