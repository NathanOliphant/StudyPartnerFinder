from django.shortcuts import render
from study.models import Subject, Course, StudyGroup
from django.shortcuts import redirect
from .forms import SearchForm
# Create your views here.
def index(request, course_id = None):
    if request.method == 'POST': # If the form has been submitted...
            form = SearchForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
                data = form.cleaned_data
                year = data['studyYear']
                semester = data['studySemester']
                subject = data['studySubject']
                selectedCourse = data['studyCourses']
                
                # Show results here.
                # Or send to new view, called course
                context = { 'course_id': selectedCourse }
                return redirect('/course/{}'.format(selectedCourse))
                #return HttpResponseRedirect('/course/', context) # Redirect after POST
    else:
        form = SearchForm() # An unbound form
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
                   'year_list': years, 'semester_list': semesters, 'form': form }
        
        return render(request, 'course/index.html', context)

def course(request, course_id = None):
    with open("testfile3.txt", "w") as file:  
        file.write("Course ID: {}".format(course_id))
    if course_id is None:
        return redirect('/search/')
    
    course_results = Course.objects.filter(isActive=1, id=course_id)
    #subject_id = course_results[0].subject
    # This should combine and users, any filters, and the sg itself:
    studygroup_results = StudyGroup.objects.filter(course=course_id)
    #subject_results = Subject.objects.filter(id=subject_id)
    
    context = { 'course_list': course_results, 'studygroup_list': studygroup_results }
    return render(request, 'course/course.html', context)