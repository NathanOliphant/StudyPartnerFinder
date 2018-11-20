from django.shortcuts import render
from .forms import StudyGroupCreationForm, StudyGroupEditForm
import simplejson
#from django import forms
# Create your views here.
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Course, StudyGroup, StudyGroupUser, BlockList
from django.shortcuts import redirect
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import GetMyJoinedStudygroups

import datetime
#from courses.views import course
from studygroups.models import Days, Message


def index(request):
    template = "studygroups/mine.html"
    # We want to return all studygroups belonging to this user.
    my_studygroups = GetMyJoinedStudygroups(request.user)
    
    if request.user.is_authenticated:    
        # Let's add some order to our studygroups.  Should we try for our groups first, in 
        # which case we need something else, or just this?  
        # It might make sense to loop through on the template, showing our owned groups,
        # then showing our joined groups.
        my_studygroups = sorted(
            my_studygroups, 
            key=lambda x: x.studygroup.course.class_name, reverse=False)
    
    context = { 'studygroup_joined_list': my_studygroups }
    
    return render(request, template, context)

# Change to
# class Add(generic.CreateView):????
@login_required
def add(request, pk=None):
    template = ''
    course = None
    c = pk
    
    myVals = {'userid': request.user.id, 'courseid': request.POST.get('course') if request.POST.get('course') is not None else c}
    
    form = StudyGroupCreationForm(request.POST or None, myVals or None)
    # Need to check if POST or GET
    # If POST, and have form data, use hidden id to created SG based on Course.
    # Otherwise, this should just load the form.
    if request.method == 'POST': # If the form has been submitted...
        # Get the course value first!!!
        
        if form.is_valid(): # All validation rules pass
            data = form.cleaned_data
            c = data['course']
           
            data['creator'] = CustomUser.objects.get(pk=request.user.id)
            
            d = Days.objects.create(days_available = data['days_available'])
            
            # List all of our form fields here.
            sg = StudyGroup.objects.create(
                post_title = data['post_title'], 
                course = data['course'], 
                creator = request.user,
                max_members = data['max_members'] if data['max_members'] is not None else 1000,  
                gender_specific = data['gender_specific' ] if data['gender_specific'] is not None else 'U' , 
                #days_available.set(d),
                hours_available_start = data['hours_available_start'] if data['hours_available_start'] is not None else datetime.time(0, 1),
                hours_available_end = data['hours_available_end'] if data['hours_available_end'] is not None else datetime.time(23, 59), 
                online_only= data['online_only'] if data['online_only'] is not None else False )
            
            if d is not None:
                sg.days_available.add(d)
                sg.save()
            
            # All members should be in the StudyGroup, so add yourself now.
            StudyGroupUser.objects.create(
                user = request.user,
                studygroup = sg)
            
            return redirect('/courses/{}'.format(c.id))
        
        else:
            if pk is not None:
                course = Course.objects.get(pk=pk)
            context = { 'form': form , 'course': course, 'pk': request.POST.get('course') if request.POST.get('course') is not None else c}
            template = 'studygroups/add.html'
            return render(request, template, context)
    
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
        
        context = { 'form': form , 'course': course, 'pk': c}
        template = 'studygroups/add.html'
    
        # Post should return us to the course?
    
        # Get takes us here:
        return render(request, template, context)

@login_required
def update(request, id=None):
    # Can only update if owner.
    # Can only update if id is passed in.
    if id is None:
        pass
    
    #myVals = {'userid': request.user.id, 'courseid': request.POST.get('course') if request.POST.get('course') is not None else id}
    studygroup = StudyGroup.objects.get(id=id)
    form = StudyGroupEditForm(request.POST or None, instance=studygroup)
    if request.method == 'POST': 
        # Confirm that we own this SG!!!
        if form.is_valid(): # All validation rules pass
            data = form.cleaned_data
            #c = data['course']
            
            # Confirm this is ours!
            sg = StudyGroup.objects.get(id=id)
            if '{}'.format(request.user.id) is '{}'.format(sg.creator):
            
                data['creator'] = CustomUser.objects.get(pk=request.user.id)
            
                d = Days.objects.create(days_available = data['days_available'])
                
                old_days_available = sg.days_available.all()
                
                #studygroup.objects.filter(id=id).update(
                sg.post_title = data['post_title']
                sg.max_members = data['max_members'] if data['max_members'] is not None else 1000
                sg.gender_specific = data['gender_specific' ] if data['gender_specific'] is not None else 'U'
                #days_available.set(d),
                sg.hours_available_start = data['hours_available_start'] if data['hours_available_start'] is not None else datetime.time(0, 1)
                sg.hours_available_end = data['hours_available_end'] if data['hours_available_end'] is not None else datetime.time(23, 59) 
                sg.online_only = data['online_only'] if data['online_only'] is not None else False
            
                if d is not None:
                    old_days_available.delete()
                    sg.days_available.add(d)
                
                sg.save()
                #form.save()
                return redirect('/studygroups/view/{}'.format(id))
            
    else:
        studygroup = StudyGroup.objects.get(id=id)
        days_available = studygroup.days_available.all()
        
        # Do we own this Studygroup?
        # if request.user.is_authenticated: 
        if '{}'.format(request.user.id) is '{}'.format(studygroup.creator):
            template = 'studygroups/update.html'
            context = { 'form': form , 'studygroup': studygroup, 'id': id, 'days_available': days_available}
            return render(request, template, context)
    
    # Days
    # Department
    # Course Name
    # Assignment????
    # Title of Post????
    # Filters . . . 
    return redirect('/studygroups/mine')

def view(request, id=None):
    if id is not None:
        mine = False
        in_group = False
        members_list = list()
        su = StudyGroupUser.objects.filter(studygroup = id).select_related('user', 'studygroup')
        # Only need the first entry to get sg details.
        studygroup =su[0].studygroup
        
        message_list = Message.objects.filter(studygroup = studygroup.id)
        
        if '{}'.format(request.user.id) is '{}'.format(studygroup.creator):
            mine = True
        
        for u in su:
            if u.user.id == request.user.id:
                in_group = True
            members_list.append(u)   
        
        owner = studygroup.creator
        
        days_available = studygroup.days_available.all()
            
    context = { 'id': id, 'studygroup': studygroup , 'message_list': message_list, 'self_owned': mine, 'am_a_member': in_group, 'members_list': members_list, 'days_available': days_available}
    template = 'studygroups/view.html'
    
    return render(request, template, context)

@login_required
def join(request, id=None):
    # We need a valid template here.
    template = 'foo.html'
    # If id is None, we need to return the user to where they came from, with a message.
    # If user fails one of the checks, return to where they came from, with a fail message.
    # Otherwise, redirect to view view.
    if id is not None:
        # We need to look at studygroup and users, so grab the StudyGroupUser object
        # so that we only need to hit the database once.
        already_in_group = False
        is_blocked = False
        sg = StudyGroup.objects.get(id = id)
        
        # We don't need to join our own groups!
        if sg.creator == request.user.id:
            already_in_group = True
        
        group_full = False
        
        if already_in_group is False and sg is not None:
            # Also confirm that we haven't already joined, as it would be a waste to join again.
            su = StudyGroupUser.objects.filter(studygroup = id, user = request.user.id).select_related('user')
            
            if su is not None:
                if len(su) >= sg.max_members:
                    group_full = True
                # Check if user already a member.
                for u in su:
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
            if not is_blocked and not already_in_group and not group_full:
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


# Receive message from user, save, and let user know success/failure.
def message(request):
    is_saved = False
    error = True
    msg = None
    # Confirm that the following are valid:
    body = request.GET.get('new_message', None)
    sg = request.GET.get('studygroup', None)
    title = request.GET.get('title', None)
        
    # Only a member of the studygroup should be able to post a message,
    # so confirm that the user is a valid member before continuing.
    # Save if valid
    if body:
        studygroup = StudyGroup.objects.get(id=sg)
        msg = Message.objects.create(
            user = request.user,
            studygroup = studygroup,
            title = title,
            body = body
            )
        msg.save()
        is_saved = True
        error = False
    
    data = {
        'is_saved': is_saved, 
        'error': error, 
        'msg_id': msg.id, 
        # We probably want our date formatted a little more user-friendly
        'msg_date': msg.date, 
        'msg_title': msg.title, 
        'msg_body': msg.body
    }
    return JsonResponse(data)

# Deactivating a studygroup will make it no longer searchable.
def deactivate(request, val):
    # Only the creator should be able to perform a deactivation, so confirm that
    # request.user is indeed the creator.
    message = {'result':''}
    with open("hello_ajax.txt", "w") as f:
        f.write('R: {}'.format(request))
        f.write('V: {}'.format(val))
    if request.is_ajax():
        with open("hello_ajax.txt", "w") as f:
            f.write('R: {}'.format(request))
            f.write('V: {}'.format(val))
        # put logic here
        #json = simplejson.dumps()   convert data into json
        return HttpResponse(message, mimetype='application/json')