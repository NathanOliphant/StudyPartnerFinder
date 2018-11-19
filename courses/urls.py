
from django.urls import path

from . import views
#url(r'^User/(?P<userid>\d+)/$', 'search.views.user_detail', name='user_details'),
urlpatterns = [
    path('', views.index, name='index'),
    #path('courses/<int:course_id>', views.course, name='courses'),
    path('<int:course_id>', views.course, name='courses'),
]

