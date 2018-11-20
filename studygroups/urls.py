from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/<slug:pk>', views.add, name='add'),
    path('add/', views.add, name='add'),
    path('update/<slug:id>', views.update, name='index'),
    path('view/<slug:id>', views.view, name='view'),
    path('join/<slug:id>', views.join, name='join'),
    path('message/', views.message, name='message')
    #url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
]