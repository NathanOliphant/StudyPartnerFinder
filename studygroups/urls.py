from django.urls import path

from . import views

# URL patterns used by the studygroups view.  
# The bulk of our app is here.
urlpatterns = [
    path('', views.index, name='index'),
    path('add/<slug:pk>', views.add, name='add'),
    path('add/', views.add, name='add'),
    path('update/<slug:pk>', views.update, name='update'),
    path('view/<slug:pk>', views.view, name='view'),
    path('join/<slug:pk>', views.join, name='join'),
    path('message/', views.message, name='message'),
    path('reloadmessages/', views.reload_messages, name='reload_messages')
    #url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
]