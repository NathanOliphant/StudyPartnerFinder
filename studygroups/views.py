from django.shortcuts import render
from .forms import StudyGroupCreationForm, StudyGroupEditForm
from django.http import JsonResponse
from .models import Course, StudyGroup, StudyGroupUser, BlockList
from django.shortcuts import redirect
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from .utils import GetMyJoinedStudygroups
import datetime
from studygroups.models import Days, Message
from django.contrib import messages


# Create your views here.
# index view displays all studygroups associated with a specific user, both created
# and joined studygroups.
def index(request):
    template = "studygroups/mine.html"
    # We want to return all studygroups belonging to this user.
    my_studygroups = list

    # If user has not been authenticated, my_studygroups should still be empty.
    if request.user.is_authenticated:
        my_studygroups = GetMyJoinedStudygroups(request.user)
        # Let's add some order to our studygroups.  Should we try for our groups first, in
        # which case we need something else, or just this?
        # It might make sense to loop through on the template, showing our owned
        # groups, then showing our joined groups.
        my_studygroups = sorted(
            my_studygroups,
            key = lambda x: x.studygroup.course.class_name, reverse = False)

    context = { 'studygroup_joined_list': my_studygroups}

    return render(request, template, context)


# You need to be logged in to add a studygroup, so we have included the
# @login_required decorator.
@login_required
def add(request, pk = None):
    template = ''
    course = None
    c = pk

    # We need to pass the user and course to the form object on a POST, so add the
    # values to a dictionary to be pass along to the form.
    myVals = {
        'userid': request.user.id,
        'courseid': request.POST.get('course') if request.POST.get('course') is not None
        else c
    }

    form = StudyGroupCreationForm(request.POST or None, myVals or None)
    # Need to check if POST or GET
    # If POST, and have form data, use hidden id to created SG based on Course.
    # Otherwise, this should just load the form.
    if request.method == 'POST':  # If the form has been submitted...
        # Get the course value first!!!
        # All validation rules pass
        if form.is_valid():
            data = form.cleaned_data
            c = data['course']

            data['creator'] = CustomUser.objects.get(pk = request.user.id)

            d = Days.objects.create(days_available = data['days_available'])

            # Create our new studygroup object with the values passed in via our form.
            sg = StudyGroup.objects.create(
                post_title = data['post_title'],
                course = data['course'],
                creator = request.user,
                max_members = data['max_members']
                    if data['max_members'] is not None else 1000,
                gender_specific = data['gender_specific' ]
                    if data['gender_specific'] is not None else 'U' ,
                # days_available.set(d),
                hours_available_start = data['hours_available_start']
                    if data['hours_available_start'] is not None else datetime.time(0, 1),
                hours_available_end = data['hours_available_end']
                    if data['hours_available_end'] is not None else datetime.time(23, 59),
                online_only = data['online_only'] if data['online_only'] is not None else False)

            # Add days as appropriate.
            if d is not None:
                sg.days_available.add(d)
                sg.save()

            # All members should be in the StudyGroup, so add yourself now.
            StudyGroupUser.objects.create(
                user = request.user,
                studygroup = sg)

            return redirect('/courses/{}'.format(c.id))

        else:
            # The form was invalid, so we need to try again.
            if pk is not None:
                course = Course.objects.get(pk = pk)
            context = {
                'form': form ,
                'course': course,
                'pk': request.POST.get('course') if request.POST.get('course') is not None
                else c
            }
            template = 'studygroups/add.html'
            return render(request, template, context)

    else:
        myVals = {'userid': request.user.id, 'courseid': c}
        form = StudyGroupCreationForm(myVals)

        if pk is not None:
            course = Course.objects.get(pk = pk)

        else:
            # Error.  Need to let the user know?
            pass

        context = { 'form': form , 'course': course, 'pk': c}
        template = 'studygroups/add.html'

        # Get takes us here:
        return render(request, template, context)


# Logged in users can update a studygroup here.
@login_required
def update(request, pk = None):
    # Can only update if owner.
    # Can only update if id is passed in.
    if pk is None:
        pass

    studygroup = StudyGroup.objects.get(id = pk)
    form = StudyGroupEditForm(request.POST or None, instance = studygroup)
    if request.method == 'POST':
        # Confirm that we own this SG!!!
        if form.is_valid():  # All validation rules pass
            data = form.cleaned_data
            # c = data['course']

            # Confirm this is ours!
            sg = StudyGroup.objects.get(id = pk)
            if request.user == sg.creator:

                data['creator'] = CustomUser.objects.get(pk = request.user.id)

                d = Days.objects.create(days_available = data['days_available'])

                old_days_available = sg.days_available.all()

                # studygroup.objects.filter(id=id).update(
                sg.post_title = data['post_title']
                sg.max_members = data['max_members'] if data['max_members'] is not None else 1000
                sg.gender_specific = data['gender_specific' ] if data['gender_specific'] is not None else 'U'
                # days_available.set(d),
                sg.hours_available_start = data['hours_available_start'] \
                    if data['hours_available_start'] is not None else datetime.time(0, 1)
                sg.hours_available_end = data['hours_available_end'] \
                    if data['hours_available_end'] is not None else datetime.time(23, 59)
                sg.online_only = data['online_only'] if data['online_only'] is not None else False
                sg.is_active = data['is_active']

                if d is not None:
                    old_days_available.delete()
                    sg.days_available.add(d)

                sg.save()
                # form.save()
                return redirect('/studygroups/view/{}'.format(pk))

    else:
        studygroup = StudyGroup.objects.get(id = pk)
        days_available = studygroup.days_available.all()

        # Do we own this Studygroup?
        # if request.user.is_authenticated:
        if request.user == studygroup.creator:
            template = 'studygroups/update.html'
            context = { 'form': form , 'studygroup': studygroup, 'id': pk, 'days_available': days_available}

            return render(request, template, context)

    return redirect('/studygroups/mine')


# view is to view a specific studygroup.
@login_required
def view(request, pk = None):
    if pk is not None:
        mine = False
        in_group = False
        members_list = list()
        # Can only view full details if you are a member.
        su = StudyGroupUser.objects.filter(studygroup = pk).select_related('user', 'studygroup')

        # Only need the first entry to get sg details.
        # We are using StudyGroupUser so that we also get a list of users.
        if su is not None and su.count() > 0:
            studygroup = su[0].studygroup
        else:
            studygroup = StudyGroup.objects.filter(id = pk).first()

        message_list = Message.objects.filter(studygroup = studygroup.id)

        if request.user == studygroup.creator:
            mine = True

        for u in su:
            if u.user == request.user:
                in_group = True
            members_list.append(u)

        # owner = studygroup.creator

        # MyModel.objects.values_list('description', flat=True)[0]
        blocked_list = list
        if request.user.is_authenticated:
            blocked_list = BlockList.objects.filter(user = request.user).values_list('blocked_user', flat = True)

        days_available = studygroup.days_available.all()

    context = { 'id': pk, 'studygroup': studygroup ,
               'message_list': message_list, 'self_owned': mine,
               'am_a_member': in_group, 'members_list': members_list,
               'days_available': days_available, 'block_list': blocked_list}
    template = 'studygroups/view.html'

    # If user is blocked, we should return a simple message and not
    # display the studygroup.

    return render(request, template, context)


# User needs to be logged in to join.
@login_required
def join(request, pk = None):
    # We need a valid template here.
    # If id is None, we need to return the user to where they came from, with a message.
    # If user fails one of the checks, return to where they came from, with a fail message.
    # Otherwise, redirect to view view.
    if pk is not None:
        # We need to look at studygroup and users, so grab the StudyGroupUser object
        # so that we only need to hit the database once.
        already_in_group = False
        is_blocked = False
        sg = StudyGroup.objects.get(id = pk)

        # We don't need to join our own groups!
        if sg.creator == request.user:
            already_in_group = True

        group_full = False

        if already_in_group is False and sg is not None:
            # Also confirm that we haven't already joined, as it would be a waste to join again.
            su = StudyGroupUser.objects.filter(studygroup = pk, user = request.user.id).select_related('user')

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
                    studygroup = sg
                )
            else:
                # Add the messages, as mentioned above
                messages.add_message(request, messages.ERROR, 'Sorry, we were unable to add you to the studygroup you requested.')
                if is_blocked:
                    messages.add_message(request, messages.ERROR, 'You are blocked from joining that studygroup.')
                if already_in_group:
                    messages.add_message(request, messages.ERROR, 'You are already in the studygroup.')
                if group_full:
                    messages.add_message(request, messages.ERROR, 'The requested studygroup is full.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            #
            # template = 'view.html'
        else:
            pass

    # Set template to return?  With error message of some sort?
    return redirect('/studygroups/view/{}'.format(pk))


@login_required
def acceptJoin(request, pk = None):
    pass


# Reload all messages for a studygroup.
@login_required
def reload_messages(request):
    sg = request.GET.get('studygroup', None)
    studygroup = StudyGroup.objects.get(id = sg)
    message_list = list(Message.objects.filter(studygroup = studygroup).values())

    data = { 'messages': message_list }

    return JsonResponse(data)


# Receive message from user, save, and let user know success/failure.
@login_required
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
        studygroup = StudyGroup.objects.get(id = sg)
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
