# accounts/urls.py
from django.urls import path

from . import views

# 
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('edit/', views.Edit.as_view(), name='edit'),
    path('view/', views.View, name='view'),
    path('', views.View, name='view'),
    path('blockuser/', views.BlockUser, name='blockuser')
]
