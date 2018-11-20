#
#    Studygroup utilities and classes used by all applications.
#
from .models import Course, StudyGroup, StudyGroupUser, BlockList, Message
from users.models import CustomUser


# StudyGroups as displayed on the page need to have full member details, so we have 
# a version that includes everything needed.
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
        
def GetMyJoinedStudygroups(user):
    my_studygroups = list()
    # First, get the StudyGroupUser objects.  This allows us to use our foreign key relation
    # later to reduce hits to the database.
    su = StudyGroupUser.objects.filter(user = user.id).select_related('studygroup')
    for e in su:
        # Without select_related(), this would make a database query for each
        # loop iteration in order to fetch the related blog for each entry.
        mine = False
        if '{}'.format(user.id) is '{}'.format(e.studygroup.creator):
            mine = True
        my_studygroups.append(SG(e.studygroup, mine=mine))
     
    # Now add the other members, although there HAS to be an easier way!
    for i, sg in enumerate(my_studygroups):
        other_members = list()
        
        sg.messages = Message.objects.filter(studygroup = sg.studygroup.id)
        
        sg.days_available = sg.studygroup.days_available.all()
        
        for e in StudyGroupUser.objects.filter(studygroup = sg.studygroup.id).select_related('user'):
            other_members.append(e.user)
        sg.members = other_members
        
        sg.owner = CustomUser.objects.filter(id = sg.studygroup.creator.id).get()
        
    return my_studygroups

def GetStudygroupsForCourse(user, course_id):
     # Need to keep track of all studygroups for this course, so put them here.
    course_studygroups = list()

    # This should combine and users, any filters, and the sg itself:
    studygroups = StudyGroup.objects.filter(course=course_id).select_related()
    for s in studygroups:
        mine = False
        
        # Get the creator.
        if '{}'.format(user.id) is '{}'.format(s.creator):
            mine = True
            
        # Get the members of the studygroup.
        other_members = list()
        in_group = False
        su = StudyGroupUser.objects.filter(studygroup = s.id).select_related('user')
        for u in su:
            if u.user.id == user.id:
                in_group = True
            other_members.append(u)
         
        days_available = s.days_available.all()
            
        owner = CustomUser.objects.filter(id = s.creator.id).get()
            
        # Now add to our list of studygroups.
        course_studygroups.append(SG(s, mine=mine, members=other_members, 
                                     owner=owner, i_am_in_group=in_group, days_available=days_available))
        
    return course_studygroups