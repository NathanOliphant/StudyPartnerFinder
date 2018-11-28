from django.shortcuts import render
from courses.views import SearchTemplate


def index(request):
    template = 'home.html'
    # Use the course SearchTemplate class as our context.
    # This means form and all our data are already included.
    context = SearchTemplate.context

    return render(request, template, context)
