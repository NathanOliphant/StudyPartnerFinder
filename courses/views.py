from django.shortcuts import render
from studygroups.models import Course, StudyGroup, StudyGroupUser, Subject
from django.shortcuts import redirect
from .forms import SearchForm
from users.models import CustomUser

# Really should put this elsewhere.  While we do not want to save it to the database, 
# we do want to be able to instantiate it in multiple places.
class SG(object):
    def __init__(self, studygroup, mine=False, members = [], owner=CustomUser, i_am_in_group = False):
        self.mine = mine
        self.studygroup = studygroup
        self.owner = owner
        self.members = members
        self.i_am_in_group = i_am_in_group
        
        
# Create your views here.
def index(request, course_id = None):
    if request.method == 'POST': # If the form has been submitted...
            form = SearchForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
                data = form.cleaned_data
                year = data['study_year']
                semester = data['study_semester']
                subject = data['study_subject']
                selected_course = data['study_courses']
                
                # Show results here.
                # Or send to new view, called course
                context = { 'course_id': selected_course }
                return redirect('/courses/{}'.format(selected_course))
                #return HttpResponseRedirect('/course/', context) # Redirect after POST
    else:
        form = SearchForm() # An unbound form
        # Courses returned should be all active, unless query requests
        # by date or semester or subject.
        # Need to return a list of years to be used for courses, and semesters.
        # Grab distinct year and semester from courses?  
        # How about a default year/semester?
        subject_results = Subject.objects.all()
        courses_results = Course.objects.filter(is_active=1)
        # We need distinct years from courses
        years = Course.objects.filter().values("year").distinct()
        semesters = Course.objects.filter().values("semester").distinct()
        
        
        #result = Contact.objects.filter(last_name__icontains=request.POST['query']) 
        # Courses should be broken into lists, based on the course subject_id
        context = { 'subject_list': subject_results, 'course_list': courses_results, 
                   'year_list': years, 'semester_list': semesters, 'form': form }
        
        return render(request, 'courses/index.html', context)

def course(request, course_id = None):
    if course_id is None:
        return redirect('/search/')
    
    # Need to keep track of all studygroups for this course, so put them here.
    course_studygroups = list()
    
    course_results = Course.objects.filter(is_active=1, id=course_id)
    #subject_id = course_results[0].subject
    with open("course_results.txt", "w") as file:  
        file.write("{} :: {}\n".format(request.user.id, course_results[0].id))
    
    # This should combine and users, any filters, and the sg itself:
    studygroups = StudyGroup.objects.filter(course=course_id).select_related()
    for s in studygroups:
        mine = False
        
        # Get the creator.
        if '{}'.format(request.user.id) is '{}'.format(s.creator):
            mine = True
            
        # Get the members of the studygroup.
        other_members = list()
        in_group = False
        su = StudyGroupUser.objects.filter(studygroup = s.id).select_related('user')
        for u in su:
            if u.user.id == request.user.id:
                in_group = True
            other_members.append(u)
         
        #with open("hello_members.txt", "w") as file:  
        #    file.write("{} in {}? {}\n".format(request.user.id, s.id, in_group))
            
        owner = CustomUser.objects.filter(id = s.creator.id).get()
            
        # Now add to our list of studygroups.
        course_studygroups.append(SG(s, mine=mine, members=other_members, 
                                     owner=owner, i_am_in_group=in_group))

    context = { 'course_list': course_results, 'studygroup_list': course_studygroups }
    return render(request, 'courses/course.html', context)