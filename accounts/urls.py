# accounts/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
   # path('signup2/', views.SignUp.as_view(), name='signup2'),
]
