from django.shortcuts import render
from studygroups.models import Course, Subject, CurrentSemester
from django.shortcuts import redirect
from .forms import SearchForm
from studygroups.utils import GetStudygroupsForCourse

class SearchTemplate(object):
    form = SearchForm() # An unbound form
    # Courses returned should be all active, unless query requests
    # by date or semester or subject.
    # Need to return a list of years to be used for courses, and semesters.
    # Grab distinct year and semester from courses?  
    # How about a default year/semester?
    current_semester = CurrentSemester.objects.get()
    subject_results = Subject.objects.all()
    courses_results = Course.objects.filter(is_active=1, 
                                            semester=current_semester.semester, 
                                            year=current_semester.year)
    # We need distinct years from courses
    #years = Course.objects.filter().values("year").distinct()
    #semesters = Course.objects.filter().values("semester").distinct()
 
    # Courses should be broken into lists, based on the course subject_id
    context = { 'subject_list': subject_results, 'course_list': courses_results, 
                #'year_list': years, 'semester_list': semesters, '
                'form': form,
                'current_semester': current_semester }

# Create your views here.
def index(request, course_id = None):
    if request.method == 'POST': # If the form has been submitted...
            form = SearchForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
                #current_semester = CurrentSemester.objects.get()
                
                data = form.cleaned_data
                #year = current_semester.year
                #semester = current_semester.semester
                #subject = data['study_subject']
                selected_course = data['study_courses']
                
                # Show results here.
                # Or send to new view, called course
                context = { 'course_id': selected_course }
                return redirect('/courses/{}'.format(selected_course))
                #return HttpResponseRedirect('/course/', context) # Redirect after POST
    else:
        form = SearchForm() # An unbound form
        
        context = SearchTemplate.context
        
        return render(request, 'courses/index.html', context)

def course(request, course_id = None):
    if course_id is None:
        return redirect('/search/')
    
    # Need to keep track of all studygroups for this course, so put them here.
    course_studygroups = GetStudygroupsForCourse(request.user, course_id)
    course_results = Course.objects.filter(is_active=1, id=course_id)
    
    context = { 'course_list': course_results, 'studygroup_list': course_studygroups }
    return render(request, 'courses/course.html', context)