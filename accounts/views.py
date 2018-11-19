from django.shortcuts import render
from users.models import CustomUser
#from studygroups.models import StudyGroupUser
from django.urls import reverse_lazy
from django.views import generic
from users.forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from studygroups.utils import GetMyJoinedStudygroups

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
    