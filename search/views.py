from django.shortcuts import render
#from django.http import HttpResponse
#from django.template import loader
from study.models import Subject, Course

# Create your views here.
def index(request):
    subject_results = Subject.objects.all()
    courses_results = Course.objects.filter(isActive=1)
    #result = Contact.objects.filter(last_name__icontains=request.POST['query']) 
    # Courses should be broken into lists, based on the course subject_id
    context = { 'subject_list': subject_results, 'course_list': courses_results }
    return render(request, 'search/index.html', context)
