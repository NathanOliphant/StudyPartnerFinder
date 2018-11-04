from django import forms
from study.models import Subject, Course

class SearchForm(forms.Form):
    MY_SEMESTER_CHOICES = (
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Fall', 'Fall')
    )
    studySemester = forms.ChoiceField(label='Semester', widget=forms.Select, choices=MY_SEMESTER_CHOICES)
    
    MY_YEAR_CHOICES = (
        (2018, 2018),
        (2019, 2019),
        (2020, 2020),
        (2021, 2021),
        (2022, 2022),
        (2023, 2023),
        (2024, 2024),
        (2025, 2025)
    )
    studyYear = forms.ChoiceField(label='Year', widget=forms.Select, choices=MY_YEAR_CHOICES)
    
    subject_list = Subject.objects.all().order_by('-name')
    SUBJECTS = {('courses_{}'.format(subject.id), subject.name) for subject in subject_list}
    # Unfortunately, sets are not sorted, so we have to clean up a little.
    SUBJECTS = sorted(list(SUBJECTS),  key=lambda SUBJECT: SUBJECT[1])
    studySubject = forms.ChoiceField(label='Subject', choices=SUBJECTS)
    
    course_list = Course.objects.all()
    COURSES = {(course.id, '{} ({})'.format(course.className, course.cNNumber)) for course in course_list if course.isActive is True}
    studyCourses = forms.ChoiceField(label='Course', choices=COURSES)
    