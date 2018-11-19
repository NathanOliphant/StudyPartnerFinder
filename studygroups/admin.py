from django.contrib import admin

# Register your models here.
from .models import StudyGroup, BlockList, StudyGroupUser, Message, Filter, StudyGroupFilter, Subject, Course, CurrentSemester

class CurrentSemesterAdmin(admin.ModelAdmin):
    #add_form = CustomCourseCreationForm
    #form = CustomUserChangeForm
    model = CurrentSemester
    list_display = ['semester', 'year']
    
class CourseAdmin(admin.ModelAdmin):
    #add_form = CustomCourseCreationForm
    #form = CustomUserChangeForm
    model = Course
    list_display = ['id', 'subject', 'class_name', 'cn_number', 'instructor', 'semester', 'year']

admin.site.register(Course, CourseAdmin)
    
class StudyGroupAdmin(admin.ModelAdmin):
    model = StudyGroup
    list_display = ['id', 'post_title', 'creator', 'course']

admin.site.register(StudyGroup, StudyGroupAdmin)    
    
class StudyGroupUserAdmin(admin.ModelAdmin):
    model = StudyGroupUser
    
    # Get name of studygroup
    def studygroup_post_title(self, obj):
        return obj.studygroup.post_title
    
    def studygroup_id(self, obj):
        return obj.studygroup.id
    
    def studygroup_course(self, obj):
        return obj.studygroup.course.class_name
    
    def user_username(self, obj):
        return obj.user.username
    
    list_display = ['studygroup_id', 'studygroup_post_title', 'studygroup_course', 'user_username' ]

admin.site.register(StudyGroupUser, StudyGroupUserAdmin)
    
admin.site.register(CurrentSemester, CurrentSemesterAdmin)
#admin.site.register(CustomUser)

#admin.site.register(CurrentSemester)
admin.site.register(BlockList)

admin.site.register(Message)
admin.site.register(Filter)
admin.site.register(StudyGroupFilter)
admin.site.register(Subject)
#admin.site.register(Course)

