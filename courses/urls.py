from django.urls import path
from . import views

# We only have two views into courses:
# All (index), or a specific course.
# To view a specific course, the course_id value is passed in.
urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:course_id>', views.course, name = 'courses'),
]

