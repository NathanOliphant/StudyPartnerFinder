#
#    Studygroup utilities and classes used by all apps.
#
from .models import StudyGroup, StudyGroupUser, BlockList, Message
from users.models import CustomUser


# StudyGroups as displayed on the page need to have full member details and
# messaging, so we have a version that includes everything needed.
class SG(object):
    def __init__(self, studygroup, days_available=False, mine=False, members = [], 
                 owner=CustomUser, i_am_in_group = False, messages = False):
        self.mine = mine
        self.studygroup = studygroup
        self.owner = owner
        self.members = members
        self.days_available = days_available
        self.i_am_in_group = i_am_in_group
        self.messages = messages

# Returns all studygroups that a user is joined to.        
def GetMyJoinedStudygroups(user):
    my_studygroups = list()
    # First, get the StudyGroupUser objects.  This allows us to use our foreign key relation
    # later to reduce hits to the database.
    su_list = StudyGroupUser.objects.filter(user = user.id).select_related('studygroup')
    for su in su_list:
        # Without select_related(), this would make a database query for each
        # loop iteration in order to fetch the related blog for each entry.
        # We need to differentiate between groups we have joined, and groups we own.
        # So set mine if user actually created the studygorup.
        mine = False
        if user.id is su.studygroup.creator.id:
            mine = True
            
        # If not mine, need to check that user is not blocked by creator of this studygroup.
        is_blocked = False
        if not mine:
            is_blocked = BlockList.objects.filter(user=su.studygroup.creator, blocked_user=user).exists()
        
        # Only add non-blocked studygroups.  
        if not is_blocked:
            my_studygroups.append(SG(su.studygroup, mine=mine))

    # Now add the other members, although there HAS to be an easier way!
    for i, sg in enumerate(my_studygroups):
        other_members = list()
        
        # Add studygroup messages.
        sg.messages = Message.objects.filter(studygroup = sg.studygroup.id)
        
        # This is the only many to many that we modeled correctly, so we can 
        # use .all() to get the related days_available for the studygroup.
        # Should have the same thing for users!
        sg.days_available = sg.studygroup.days_available.all()
        
        # Add your other members.
        for e in StudyGroupUser.objects.filter(studygroup = sg.studygroup.id).select_related('user'):
            other_members.append(e.user)
        sg.members = other_members
        
        # Even though we have this in studygroup.creator, adding owner here as well.
        # Do I remember why?  Of course not.
        sg.owner = CustomUser.objects.filter(id = sg.studygroup.creator.id).get()
        
    return my_studygroups

# Return studygroups associated with a specific course rather than associated with 
# a specific user. 
def GetStudygroupsForCourse(user, course_id):
    # Need to keep track of all studygroups for this course, so put them here.
    course_studygroups = list()

    # This should combine and users, any filters, and the sg itself:
    studygroups = StudyGroup.objects.filter(course=course_id).select_related()
    for s in studygroups:
        mine = False
        
        # Get the creator.
        if user == s.creator:
            mine = True
            
        # Get the members of the studygroup.
        other_members = list()
        in_group = False
        su = StudyGroupUser.objects.filter(studygroup = s.id).select_related('user')
        for u in su:
            if u.user == user:
                in_group = True
            other_members.append(u)

        days_available = s.days_available.all()
            
        owner = CustomUser.objects.filter(id = s.creator.id).get()
        
        # If not mine, need to check that user is not blocked by creator of this studygroup.
        is_blocked = False
        # Non-authenticated users will not show up, so skip if not authenticated.
        if user.is_authenticated:
            if not mine:
                is_blocked = BlockList.objects.filter(user=u.studygroup.creator, blocked_user=user).exists()
         
        # Now check for gender filter.
        if u.studygroup.gender_specific != 'U' and user.gender in ('M', 'F', 'N'):
            if user.gender != u.studygroup.gender_specific:
                is_blocked = True 
            
        if not is_blocked:
            # Now add to our list of studygroups.
            course_studygroups.append(SG(s, mine=mine, members=other_members, 
                                     owner=owner, i_am_in_group=in_group, days_available=days_available))
        
    return course_studygroups