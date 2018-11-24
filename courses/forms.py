from django import forms
from studygroups.models import Subject, Course, CurrentSemester

class SearchForm(forms.Form):
    class Meta:
        model = Course
        # The only fields we want to search on for a course are subject and the actual 
        #course name, so limit it here in fields.
        fields=['study_subject', 'study_courses']
     
    # Course/StudyGroup search relies on the course and subject, so we will pull 
    # those in here.
    SUBJECTS = {
        ('courses_{}'.format(subject.id), subject.name) for subject in Subject.objects.all()}
    # Unfortunately, sets are not sorted after creating above SUBJECTS dict, so we have 
    # to clean up a little.
    SUBJECTS = sorted(list(SUBJECTS),  key=lambda SUBJECT: SUBJECT[1])
    study_subject = forms.ChoiceField(label='Subject', choices=SUBJECTS)
    
    # Since we only offer search for the current semester, limit our courses
    # by the first value of current_semester.
    # CurrentSemester should only contain one entry, so 
    # should be able to use first or last to get in a format
    # that is easy to use.
    current_semester = CurrentSemester.objects.first()
    
    COURSES = {
        (course.id, '{} ({})'.format(course.class_name, course.cn_number)) 
        for course in Course.objects.filter(
            semester = current_semester.semester, 
            year = current_semester.year, 
            is_active = True)}
    study_courses = forms.ChoiceField(label='Course', choices=COURSES)
    
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
       
    