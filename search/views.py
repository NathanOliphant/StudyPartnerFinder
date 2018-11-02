from django.shortcuts import render
#from django.http import HttpResponse
#from django.template import loader
from study.models import Subject, Course

# Create your views here.
def index(request):
    # Courses returned should be all active, unless query requests
    # by date or semester or subject.
    # Need to return a list of years to be used for courses, and semesters.
    # Grab distinct year and semester from courses?  
    # How about a default year/semester?
    subject_results = Subject.objects.all()
    courses_results = Course.objects.filter(isActive=1)
    # We need distinct years from courses
    years = Course.objects.filter().values("year").distinct()
    semesters = Course.objects.filter().values("semester").distinct()
    
    
    #result = Contact.objects.filter(last_name__icontains=request.POST['query']) 
    # Courses should be broken into lists, based on the course subject_id
    context = { 'subject_list': subject_results, 'course_list': courses_results, 
               'year_list': years, 'semester_list': semesters }
    return render(request, 'search/index.html', context)
