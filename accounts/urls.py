# accounts/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('edit/<slug:pk>', views.Edit.as_view(), name='edit'),
    path('view/<slug:pk>', views.View.as_view(), name='view'),
]
