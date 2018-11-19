# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    username = forms.CharField(widget = forms.HiddenInput(), required = False)

    
    MY_GENDER_CHOICES = (
        ('U', 'Select a gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Nonbinary')
    )
    gender = forms.ChoiceField(choices=MY_GENDER_CHOICES,  required=False, help_text='Optional.', label='Gender', initial='U')
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'gender')
        
    #def __init__(self, *args, **kwargs):
    #    super(UserCreationForm, self).__init__(*args, **kwargs)
        # We want to validate that username is start of email address,
        # and email address is humboldt.edu.
    #    uname = '{}'.format(self.fields['email'])
    #    uname = uname.split("@", 1)
    #    if args is not None:
    #        with open("hello_email.txt", "w+") as f:
    #            f.write('email == {}\n'.format(args['email']))
        # Confirm that uname matches form's username.
        # Confirm that email is humboldt.edu.
        # If not humboldt.edu, form fails validation.
        
class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    MY_GENDER_CHOICES = (
        ('U', 'Select a gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Nonbinary')
    )
    gender = forms.ChoiceField(choices=MY_GENDER_CHOICES,  required=False, help_text='Optional.', label='Gender', initial='U')
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'gender')
        
        
        