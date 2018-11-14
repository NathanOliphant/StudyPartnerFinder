from django.shortcuts import render
from users.models import CustomUser
from studygroups.models import StudyGroupUser
from django.urls import reverse_lazy
from django.views import generic
from users.forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# 
class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
 
class Edit(LoginRequiredMixin, generic.edit.UpdateView):
    # Make sure only the registered user can change this!
    fields = ['first_name', 'last_name', 'gender']
    model = CustomUser
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    # We are already at accounts, so only need the view portion.
    success_url = reverse_lazy('view')
    template_name = 'users/edit.html'
    
    def get_object(self):
        return self.request.user
    
# StudyGroups as displayed on the page need to have full member details, so we have 
# a version that includes everything needed.
class SG(object):
    def __init__(self, studygroup, mine=False, members = [], owner=CustomUser):
        self.mine = mine
        self.studygroup = studygroup
        self.owner = owner
        self.members = members

# Only logged-in users should be able to view user details, so use
# @login_required.  Were this a class, we would use LoginRequiredMixin instead.
@login_required
def View(request):
    template_name = 'users/index.html'
    #
    my_studygroups = list()
    # First, get the StudyGroupUser objects.  This allows us to use our foreign key relation
    # later to reduce hits to the database.
    su = StudyGroupUser.objects.filter(user = request.user.id).select_related('studygroup')
    for e in su:
        # Without select_related(), this would make a database query for each
        # loop iteration in order to fetch the related blog for each entry.
        mine = False
        if '{}'.format(request.user.id) is '{}'.format(e.studygroup.creator):
            mine = True
        my_studygroups.append(SG(e.studygroup, mine=mine))
     
    # Now add the other members, although there HAS to be an easier way!
    for sg in my_studygroups:
        other_members = list()
        for e in StudyGroupUser.objects.filter(studygroup = sg.studygroup.id).select_related('user'):
            other_members.append(e.user)
        sg.members = other_members
        
        sg.owner = CustomUser.objects.filter(id = sg.studygroup.creator.id).get()
        
    # Let's add some order to our studygroups.  Should we try for our groups first, in 
    # which case we need something else, or just this?  
    # It might make sense to loop through on the template, showing our owned groups,
    # then showing our joined groups.
    my_studygroups = sorted(
                            my_studygroups, 
                            key=lambda x: x.studygroup.course.class_name, reverse=False)
        
    context = { 'user': request.user, 'studygroup_joined_list': my_studygroups }
        
    return render(request, template_name, context)
    