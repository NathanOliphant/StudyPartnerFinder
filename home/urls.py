from django.urls import path

from . import views
#url(r'^User/(?P<userid>\d+)/$', 'search.views.user_detail', name='user_details'),
urlpatterns = [
    path('', views.index, name='index'),
    #path('/', views.index, name='index'),
]

