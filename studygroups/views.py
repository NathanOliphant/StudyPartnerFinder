from django.shortcuts import render
from .forms import StudyGroupCreationForm
from django import forms
# Create your views here.
from django.http import HttpResponse
from .models import Course, StudyGroup, StudyGroupUser, BlockList
from django.shortcuts import redirect
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import datetime, time

def index(request):
    return HttpResponse("Hello, world. You're at the studygroup index.")

# Change to
# class Add(generic.CreateView):????
@login_required
def add(request, pk=None):
    template = ''
    course = None
    c = pk
    
    
    # Need to check if POST or GET
    # If POST, and have form data, use hidden id to created SG based on Course.
    # Otherwise, this should just load the form.
    if request.method == 'POST': # If the form has been submitted...
        # Get the course value first!!!
        
        #with open("hello_post.txt", "w+") as f:
        #    f.write('Post == {}\n'.format(request.POST))
        
        myVals = {'userid': request.user.id, 'courseid': request.POST.get('course')}
        form = StudyGroupCreationForm(request.POST, myVals)#, course_id = request.POST.get('course'))#, my_user = request.user) # A form bound to the POST data
        
        
        if form.is_valid(): # All validation rules pass
            data = form.cleaned_data
            c = data['course']
           
            data['creator'] = CustomUser.objects.get(pk=request.user.id)
            
            #with open("hello_data.txt", "w+") as f:
            #    f.write('Post == {}\n'.format(data))
            
            # List all of our form fields here.
            sg = StudyGroup.objects.create(
                post_title = data['post_title'], 
                course = data['course'], 
                creator = request.user,
                max_members = data['max_members'] if data['max_members'] is not None else 1000,  
                gender_specific = data['gender_specific' ] if data['gender_specific'] is not None else 'U' , 
                days_available = data['days_available'] if data['days_available'] is not None else 'Friday',
                hours_available_start = data['hours_available_start'] if data['hours_available_start'] is not None else datetime.time(0, 1),
                hours_available_end = data['hours_available_end'] if data['hours_available_end'] is not None else datetime.time(23, 59), 
                online_only= data['online_only'] if data['online_only'] is not None else False )
            
            # All members should be in the StudyGroup, so add yourself now.
            su = StudyGroupUser.objects.create(
                user = request.user,
                studygroup = sg)
            
        return redirect('/courses/{}'.format(c.id))
    
    else:
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
        template = 'studygroups/add.html'
    
        # Post should return us to the course?
    
        # Get takes us here:
        return render(request, template, context)

@login_required
def update(request, id=None):
    # Can only update if owner.
    # Department
    # Course Name
    # Assignment????
    # Title of Post????
    # Filters . . . 
    return HttpResponse("Hello, world. You're at the studygroup update.")

def view(request, id=None):
    #with open("sg_view_id.txt", "w+") as f:
    #    f.write('Post == {}\n'.format(id))
    if id is not None:
        #with open("sg_view_id2.txt", "w+") as f:
        #    f.write('Post == {}\n'.format(id))
        mine = False
        in_group = False
        members_list = list()
        su = StudyGroupUser.objects.filter(studygroup = id).select_related('user', 'studygroup')
        # Only need the first entry to get sg details.
        studygroup =su[0].studygroup
        #with open("sg_view_sg.txt", "w+") as f:
        #    f.write('SG == {}\n'.format(studygroup.id))
        
        if '{}'.format(request.user.id) is '{}'.format(studygroup.creator):
            mine = True
        #with open("sg_view_mine.txt", "w+") as f:
        #    f.write('Mine == {}\n'.format(mine))
        for u in su:
            if u.user.id == request.user.id:
                in_group = True
            members_list.append(u)   
        #with open("sg_view_members_in_group.txt", "w+") as f:
        #    f.write("in group? {}".format(in_group))
        owner = studygroup.creator
            
    context = { 'id': id, 'studygroup': studygroup , 'self_owned': mine, 'am_a_member': in_group, 'members_list': members_list}
    template = 'studygroups/view.html'
    
    return render(request, template, context)

@login_required
def join(request, id=None):
    # We need a valid template here.
    template = 'foo.html'
    # If id is None, we need to return the user to where they came from, with a message.
    # If user fails one of the checks, return to where they came from, with a fail message.
    # Otherwise, redirect to view view.
    with open("sg_join_id.txt", "w+") as f:
        f.write('Post == {}\n'.format(id))
    if id is not None:
        # We need to look at studygroup and users, so grab the StudyGroupUser object
        # so that we only need to hit the database once.
        already_in_group = False
        is_blocked = False
        sg = StudyGroup.objects.get(id = id)
        
        with open("sg_join_uname.txt", "w+") as f:
            f.write('SG Username? {}\n'.format(sg.creator.username))
            
        # We don't need to join our own groups!
        if sg.creator == request.user.id:
            already_in_group = True
        
        with open("sg_join_id.txt", "w+") as f:
            f.write('Already in group? {}\n'.format(already_in_group))
        
        if already_in_group is False and sg is not None:
            # Also confirm that we haven't already joined, as it would be a waste to join again.
            su = StudyGroupUser.objects.filter(studygroup = id, user = request.user.id).select_related('user')
            with open("sg_join_users.txt", "w+") as f:
                if su is not None:
                    # Check if user already a member.
                    for u in su:
                        f.write('User? {}\n'.format(u.user.username))
                        f.write('Users {} and {}  match? {}\n'.format(u.user.id, request.user.id, u.user.id == request.user.id))
                        if u.user.id == request.user.id:
                            already_in_group = True
            # Also confirm that user hasn't been blocked by the creator of this SG.
            bu = BlockList.objects.filter(blocked_user = request.user.id)
            if bu is not None:
                for u in bu:
                    if u.user.id == sg.creator.id and u.blocked_user.id == request.user.id:
                        is_blocked = True
                    
            # If blocked, should notify user that they cannot join this group.
            # If already a member, should notify that they are already a member.
            # Otherwise, add to the StudygroupUser table.
            if not is_blocked and not already_in_group:
            #with open("sg_join_create.txt", "w+") as f:
            #    f.write("About to create StudyGroupUser")
                s = StudyGroupUser.objects.create(
                    user = request.user,
                    studygroup = sg)
            
            # 
            template = 'view.html'
        else:
            pass
            # Set template to return?  With error message of some sort?
    return redirect('/studygroups/view/{}'.format(id))

@login_required
def acceptJoin(request, id=None):
    pass