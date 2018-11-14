from django import forms
from studygroups.models import Subject, Course

class SearchForm(forms.Form):
    MY_SEMESTER_CHOICES = (
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Fall', 'Fall')
    )
    study_semester = forms.ChoiceField(label='Semester', widget=forms.Select, choices=MY_SEMESTER_CHOICES)
    
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
    study_year = forms.ChoiceField(label='Year', widget=forms.Select, choices=MY_YEAR_CHOICES)
    
    subject_list = Subject.objects.all().order_by('-name')
    SUBJECTS = {('courses_{}'.format(subject.id), subject.name) for subject in subject_list}
    # Unfortunately, sets are not sorted, so we have to clean up a little.
    SUBJECTS = sorted(list(SUBJECTS),  key=lambda SUBJECT: SUBJECT[1])
    study_subject = forms.ChoiceField(label='Subject', choices=SUBJECTS)
    
    course_list = Course.objects.all()
    COURSES = {(course.id, '{} ({})'.format(course.class_name, course.cn_number)) for course in course_list if course.is_active is True}
    study_courses = forms.ChoiceField(label='Course', choices=COURSES)
    