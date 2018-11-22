from django.shortcuts import render
from users.models import CustomUser
#from studygroups.models import StudyGroupUser
from django.urls import reverse_lazy
from django.views import generic
from users.forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from studygroups.utils import GetMyJoinedStudygroups
from django.http import JsonResponse
from django.http import HttpResponse
from studygroups.models import BlockList

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

# Only logged-in users should be able to view user details, so use
# @login_required.  Were this a class, we would use LoginRequiredMixin instead.
@login_required
def View(request):
    template_name = 'users/index.html'
    #
    my_studygroups = GetMyJoinedStudygroups(request.user)
        
    # Let's add some order to our studygroups.  Should we try for our groups first, in 
    # which case we need something else, or just this?  
    # It might make sense to loop through on the template, showing our owned groups,
    # then showing our joined groups.
    my_studygroups = sorted(
        my_studygroups, 
        key=lambda x: x.studygroup.course.class_name, reverse=False)
        
    context = { 'user': request.user, 'studygroup_joined_list': my_studygroups }
        
    return render(request, template_name, context)
    
    
# Blocking a user means that they will no longer be able to see your studygroups
# or join your studygroups.
def BlockUser(request):
    # We should verify all of these.
    # Only the creator should be able to perform a deactivation, so confirm that
    # request.user is indeed the creator.
    is_blocked = False
    
    blockee = request.GET.get('user')
    blockee = CustomUser.objects.filter(id=blockee).get()
    # Either block or unblock.
    block_action = request.GET.get('block_action')
    sg = request.GET.get('studygroup')
    
    # If the request is to block, and we are already blocked, we do not need to do anything.
    block_exists = BlockList.objects.filter(
        user= request.user.id, 
        blocked_user=blockee).exists()
        
    if block_action == 'block':
        if not block_exists:
            bl = BlockList.objects.create(user = request.user, blocked_user = blockee)
            bl.save()
            
        is_blocked = True
        
    elif block_action == 'unblock':
        if block_exists:
            BlockList.objects.filter(user = request.user.id, blocked_user = blockee).delete() 
    else:
        pass
        # Only need this if we want to catch invalid calls.
    
    data = {'blocked': is_blocked}
    

        # put logic here
        #json = simplejson.dumps()   convert data into json
    return JsonResponse(data)