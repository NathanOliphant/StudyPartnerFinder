from django.shortcuts import render
from users.models import CustomUser
from django.contrib.auth.models import AbstractUser
from study.models import StudyGroup, StudyGroupUser, StudyGroupFilter

# accounts/views.py
#from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from django.views.generic.detail import DetailView

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    
class Edit(generic.edit.UpdateView):
    # Make sure only the registered user can change this!
    fields = ['first_name', 'last_name', 'gender']
    model = CustomUser
    #form_class = CustomUserChangeForm
    
    success_url = reverse_lazy('/accounts/view/')
    template_name = 'user/edit.html'

class SG(object):
    def __init__(self, studygroup, mine=False, members = [], owner=CustomUser):
        self.mine = mine
        self.studygroup = studygroup
        self.owner = owner
        self.members = members

def View(request, id=None):
    #template_name = 'contact.html'
    #form_class = CustomUserChangeForm
    #model = CustomUser
    #fields = ['id']
    #user = CustomUser
    #success_url = reverse_lazy('login')
    template_name = 'user/index.html'
    
    # Get all studygroups you are a member of.
    # Get all members of those studygroups (CustomUser first/last/email/id, studygroup ID)
    
    #user = CustomUser.objects.select_related()
    #studygroups_member = StudyGroupUser.objects.filter(userId = request.user.id)
    my_studygroups = list()
    #memberships = list()
    #other_members = list()
    # First, get the studygroups.
    su = StudyGroupUser.objects.filter(userId = request.user.id).select_related('studyGroupId')
    for e in su:
    # Without select_related(), this would make a database query for each
    # loop iteration in order to fetch the related blog for each entry.
        #filters = StudyGroupFilter.objects.filter(studyGroupId = e.studyGroupId)
        #memberships.append(e.studyGroupId)
        #other_members.append(e.userId)
        mine = False
        
        #my_owner = e.creatorUserId
        
        #tester = '{}'.format(request.user.id)
        #tester2 = '{}'.format(e.studyGroupId.creatorUserId)
        #with open("hello_{}_{}.txt".format(tester, tester2), "w") as f:
        #    f.write('{} is {}?'.format(tester, tester2))
        if '{}'.format(request.user.id) is '{}'.format(e.studyGroupId.creatorUserId):
            mine = True
        my_studygroups.append(SG(e.studyGroupId, mine=mine))
     
    # Now add the other members, although there HAS to be an easier way!
    for sg in my_studygroups:
        other_members = list()
        for e in StudyGroupUser.objects.filter(studyGroupId = sg.studygroup.id).select_related('userId'):
            other_members.append(e.userId)
        sg.members = other_members
        
        sg.owner = CustomUser.objects.filter(id = sg.studygroup.creatorUserId.id).get()
        #with open("hello.txt", "w") as f:
        #    f.write('{}'.format(sg.owner.email))
        #for member in sg.members:
        #    with open("hello_{}.txt".format(member.id), "w") as f:
        #        f.write('{}'.format(member.email))
    
    # Let's add some order to our studygroups.  Should we try for our groups first, in 
    # which case we need something else, or just this?  
    # It might make sense to loop through on the template, showing our owned groups,
    # then showing our joined groups.
    my_studygroups = sorted(
                            my_studygroups, 
                            key=lambda x: x.studygroup.course.className, reverse=False)
    
    # Each studygroup should have:
    # 1. Studygroup details
    # 2. Membership list with member details
    # 3. Studygroup filters list
    # We also need all filters for the studygroups, so get those here.  
    #for e in StudyGroupFilter.objects.filter(studyGroupId = request.user.id).select_related('studyGroupId', 'userId'):
    # Without select_related(), this would make a database query for each
    # loop iteration in order to fetch the related blog for each entry.
    #    memberships.append(e.studyGroupId)
    #    other_members.append(e.userId)
    
    #studygroups_member = StudyGroupUser.objects.filter(userId = request.user.id).select_related('studyGroupId')
    #memberships = list()
    
    #with open("hello.txt", "w") as f:
    #    f.write('{}'.format(z[0].id))
    #z = studygroups_member.StudyGroup
    
    #for sg in studygroups_member:
        # Get list of 
    #    memberships.append(StudyGroup.objects.get(id = sg.studyGroupId.pk))
        
    #studygroups_owned = StudyGroup.objects.filter(creatorUserId = request.user.id, isActive = True)
    #sm = studygroups_member.studyGroupId
    #with open("hello.txt", "w") as f:
     #    f.write('{}'.format(len(studygroups_member))) 
    #    for s in sm: 
            #f.write(s.CustomUser.id  ) 
    #        f.write(s  ) 
            #f.write(s.StudyGroup.course.className  ) 
    #studygroups_joined = StudyGroupUser.objects.filter(userId = self.request.user.id).all()
        
    context = { 'user': request.user, 'studygroup_joined_list': my_studygroups }
        
    return render(request, template_name, context)
        #return ([self.request.user, studygroups_owned, studygroups_member])
    