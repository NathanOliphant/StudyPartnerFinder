from django.contrib import admin

# Register your models here.
from .models import User, StudyGroup, BlockList, StudyGroupUser, Message, Filter, StudyGroupFilter, Subject, Course

admin.site.register(User)
admin.site.register(StudyGroup)
admin.site.register(BlockList)
admin.site.register(StudyGroupUser)
admin.site.register(Message)
admin.site.register(Filter)
admin.site.register(StudyGroupFilter)
admin.site.register(Subject)
admin.site.register(Course)
