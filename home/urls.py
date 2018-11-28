from django.urls import path

# Home is just the default landing page, so only a single view.
from . import views
# url(r'^User/(?P<userid>\d+)/$', 'search.views.user_detail', name='user_details'),
urlpatterns = [
    path('', views.index, name = 'index'),
]

