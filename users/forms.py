# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

MY_GENDER_CHOICES = (
    ('U', 'Select a gender'),
    ('M', 'Male'),
    ('F', 'Female'),
    ('N', 'Nonbinary')
)
# Forms for creating or editing our custom users.
# Will need to switch gender choices to using genderchoice table.
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    username = forms.CharField(widget = forms.HiddenInput(), required = False)
    gender = forms.ChoiceField(
        choices=MY_GENDER_CHOICES,  
        required=False, 
        help_text='Optional.', 
        label='Gender', 
        initial='U')
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'gender')
        
class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    gender = forms.ChoiceField(
        choices=MY_GENDER_CHOICES,  
        required=False, 
        help_text='Optional.', 
        label='Gender', 
        initial='U')
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'gender')
        
        
        