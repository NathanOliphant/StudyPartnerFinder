from django.shortcuts import render
# accounts/views.py
#from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from users.forms import CustomUserCreationForm#, CustomSignUpForm


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    
# Create your views here.
#from django.contrib.auth import login, authenticate
#from django.shortcuts import redirect
# def SignUp2(request):
#     if request.method == 'POST':
#         form = CustomSignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = CustomSignUpForm()
#     return render(request, 'signup2.html', {'form': form})