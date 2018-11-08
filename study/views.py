from django.shortcuts import render
from .forms import  StudyGroupCreationForm
from django import forms
# Create your views here.
from django.http import HttpResponse
from .models import Course, StudyGroup
from django.shortcuts import redirect
from users.models import CustomUser

def index(request):
    return HttpResponse("Hello, world. You're at the studygroup index.")

# Change to
# class Add(generic.CreateView):????
def add(request, pk=None):
    template = ''
    course = None
    c = pk
    with open("hello.txt", "w") as f:
        f.write('{}'.format(c)) 
    with open("hello13.txt", "w") as f:
        f.write('{}'.format(request.user.id)) 
    # Need to check if POST or GET
    # If POST, and have form data, use hidden id to created SG based on Course.
    # Otherwise, this should just load the form.
    if request.method == 'POST': # If the form has been submitted...
        # Get the course value first!!!
        #with open("hello123.txt", "w") as f:
        #    f.write('{}\n{}'.format(request.user.id, request.POST.get('course')))
        #request.course_id = request.POST.get('course')
        #with open("hello1234.txt", "w") as f:
        #    for key in request.POST:
        #        value = request.POST[key]
        #        f.write('{} =={}\n'.format(key, value))
        #    f.write('userid: {}'.format(request.user.id))
        myVals = {'userid': request.user.id, 'courseid': request.POST.get('course')}
        form = StudyGroupCreationForm(request.POST, myVals)#, course_id = request.POST.get('course'))#, my_user = request.user) # A form bound to the POST data
        
        
        if form.is_valid(): # All validation rules pass
            data = form.cleaned_data
            c = data['course']
            
            #course = Course.objects.get(id=c)
            #with open("hello5.txt", "w") as f:
            #        f.write('{}'.format(c)) 
            #data['course'] = course
            
            #with open("hello2.txt", "w") as f:
            #        f.write('{}'.format(c)) 
            data['creatorUserId'] = CustomUser.objects.get(pk=request.user.id)
            with open("hello_data.txt", "w") as f:
                    f.write('{}'.format(data)) 
                # Save this SG and return to course
                
            # List all of our form fields here.
            sg = StudyGroup.objects.create(
                postTitle = data['postTitle'], 
                course = data['course'], 
                creatorUserId = data['creatorUserId'],
                maxMembers = data['maxMembers'] if data['maxMembers'] is not None else 1000,  
                genderSpecific = data['genderSpecific' ] if data['genderSpecific'] is not None else 'U' , 
                daysAvailable = data['daysAvailable']if data['daysAvailable'] is not None else 'Friday',
                hoursMondayStart = data['hoursMondayStart'] if data['hoursMondayStart'] is not None else 0,  
                
                hoursMondayEnd = data['hoursMondayEnd'] if data['hoursMondayEnd'] is not None else 2359,  
                
                hoursTuesdayStart = data['hoursTuesdayStart'] if data['hoursTuesdayStart'] is not None else 0,
                
                hoursTuesdayEnd = data['hoursTuesdayEnd'] if data['hoursTuesdayEnd'] is not None else 2359,  
                
                hoursWednesdayStart= data['hoursWednesdayStart'] if data['hoursWednesdayStart'] is not None else 0,  
                
                hoursWednesdayEnd= data['hoursWednesdayEnd'] if data['hoursWednesdayEnd'] is not None else 2359,  
                
                hoursThursdayStart= data['hoursThursdayStart'] if data['hoursThursdayStart'] is not None else 0,  
                hoursThursdayEnd= data['hoursThursdayEnd'] if data['hoursThursdayEnd'] is not None else 2359,  
                 
                hoursFridayStart= data['hoursFridayStart'] if data['hoursFridayStart'] is not None else 0,
                 
                hoursFridayEnd= data['hoursFridayEnd'] if data['hoursFridayEnd'] is not None else 2359,
                 
                hoursSaturdayStart= data['hoursSaturdayStart'] if data['hoursSaturdayStart'] is not None else 0, 
                 
                hoursSaturdayEnd  = data['hoursSaturdayEnd'] if data['hoursSaturdayEnd'] is not None else 2359,
                 
                hoursSundayStart= data['hoursSundayStart'] if data['hoursSundayStart'] is not None else 0, 
                 
                hoursSundayEnd= data['hoursSundayEnd'] if data['hoursSundayEnd'] is not None else 2359,  
                onlineOnly= data['onlineOnly'] if data['onlineOnly'] is not None else False )
            #p = StudyGroup(data)
            #
            #p = p.objects.get_or_create()
            #with open("hello3.txt", "w") as f:
            #        f.write('{}'.format(p)) 
            
        return redirect('/course/{}'.format(c.id))
    
    else:
        with open("hello12.txt", "w") as f:
            f.write('{}'.format(c)) 
            f.write('{}'.format(request.user))
            
        myVals = {'userid': request.user.id, 'courseid': c}
        form = StudyGroupCreationForm(myVals)
    # If ID passed, base course on id
    # Can only add if registered.
    # Department
    # Course Name
    # Assignment????
    # Title of Post????
    # Filters . . . 
        # Get a proper template!!!!
        if pk is not None:
            course = Course.objects.get(pk=pk)
        #form.course = forms.CharField(label='Course', widget = forms.HiddenInput())
        #form.course.value = id
    #else:
    #    course_list = Course.objects.all()
    #    COURSES = {(course.id, '{} ({})'.format(course.className, course.cNNumber)) for course in course_list if course.isActive is True}
    #    course = forms.ChoiceField(label='Course', choices=COURSES)
        else:
        # Error.  Need to let the user know?
            pass
        
        context = { 'form': form , 'course': course}
        template = 'study/add.html'
    
        with open("hello6.txt", "w") as f:
                    f.write('{}'.format(course.id))
    
        # Post should return us to the course?
    
        # Get takes us here:
        return render(request, template, context)

def update(request, id=None):
    # Can only update if owner.
    # Department
    # Course Name
    # Assignment????
    # Title of Post????
    # Filters . . . 
    return HttpResponse("Hello, world. You're at the studygroup update.")

def view(request, id=None):
    # Get details from id passed.
    return HttpResponse("Hello, world. You're at the studygroup details.")

def requestJoin(request, id=None):
    pass

def acceptJoin(request, id=None):
    pass