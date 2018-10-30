# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    
    
    MY_GENDER_CHOICES = (
        ('U', 'Select a gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Nonbinary')
    )
    gender = forms.ChoiceField(choices=MY_GENDER_CHOICES,  required=False, help_text='Optional.', label='Gender', initial='U')
    
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'is_staff', 'first_name', 'last_name', 'college', 'gender')
        

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_staff')