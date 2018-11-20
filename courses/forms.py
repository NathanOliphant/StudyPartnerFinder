from django import forms
from studygroups.models import Subject, Course, CurrentSemester

class SearchForm(forms.Form):
    class Meta:
        model = Course
        fields=['study_subject', 'study_courses']
        
    subject_list = Subject.objects.all().order_by('-name')
    SUBJECTS = {('courses_{}'.format(subject.id), subject.name) for subject in subject_list}
    # Unfortunately, sets are not sorted, so we have to clean up a little.
    SUBJECTS = sorted(list(SUBJECTS),  key=lambda SUBJECT: SUBJECT[1])
    study_subject = forms.ChoiceField(label='Subject', choices=SUBJECTS)
    
    course_list = Course.objects.all()
    COURSES = {(course.id, '{} ({})'.format(course.class_name, course.cn_number)) for course in course_list if course.is_active is True}
    study_courses = forms.ChoiceField(label='Course', choices=COURSES)
    
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
       
    