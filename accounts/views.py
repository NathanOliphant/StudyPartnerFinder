from django.shortcuts import render
from users.models import CustomUser
from django.contrib.auth.models import AbstractUser

# accounts/views.py
#from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from django.views.generic.detail import DetailView

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    
class Edit(generic.edit.UpdateView):
    # Make sure only the registered user can change this!
    fields = ['first_name', 'last_name', 'gender']
    model = CustomUser
    #form_class = CustomUserChangeForm
    
    success_url = reverse_lazy('login')
    template_name = 'user/edit.html'

class View(DetailView):
    #template_name = 'contact.html'
    #form_class = CustomUserChangeForm
    #model = CustomUser
    fields = ['id']
    user = CustomUser
    
    #success_url = reverse_lazy('login')
    template_name = 'user/index.html'
    
    def get_object(self):
        return self.request.user
    