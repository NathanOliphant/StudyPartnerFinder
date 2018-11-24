from django import forms
from studygroups.models import Course, StudyGroup
from users.models import CustomUser

#
#    Forms used in studygroups app.
#

# The following constants (MY_GENDER_CHOICES, MY_DAY_CHOICES)
# should probably be replaced by database entries.
# Perhaps version 2?
MY_GENDER_CHOICES = (
         ('U', 'Undeclared'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Nonbinary')
)

MY_DAY_CHOICES = (
         ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), 
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    )
    
# Form used for studygroup creation.  All fields will be validated before the new object
# can be created.
class StudyGroupCreationForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        # Limit the studygroup fields to be displayed in the form.
        fields=['post_title', 'course', 'max_members', 'gender_specific' ,'days_available',
                'hours_available_start', 'hours_available_end', 'online_only']
        exclude = ['creator']
    
    post_title = forms.CharField(label='Post Title', required=True, help_text='Required')
    # We want this hidden.  Will display the course details via View.
    #course = forms.CharField(label='Course')
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(pk=1),
        widget = forms.HiddenInput(), required=False)
    # Creator is a CustomUser object, so use ModelChoiceField.
    creator = forms.ModelChoiceField(
        queryset = CustomUser.objects.filter(pk=1), 
        widget = forms.HiddenInput, required=False)
    max_members = forms.IntegerField(required=False, help_text='Optional.')
    gender_specific = forms.ChoiceField(label='Gender', widget=forms.Select, choices=MY_GENDER_CHOICES, 
                                     required=False, help_text='Optional.')
    days_available = forms.MultipleChoiceField(label='Days Available', 
                                              widget=forms.SelectMultiple, 
                                              choices=MY_DAY_CHOICES, 
                                              required=False, 
                                              help_text='Optional.')
    # hourse_available_start and hours_available_end should be the same format,
    # but we are currently testing different fields here.
    hours_available_start = forms.TimeInput(format='%H:%M')
    hours_available_end = forms.TimeField(
        widget=forms.TimeInput,
        label='Hours Available End', 
        required=False,
        help_text='Optional'
    )
    online_only = forms.BooleanField(required=False, help_text='Optional.')
    
    def __init__(self, *args, **kwargs):
        super(StudyGroupCreationForm, self).__init__(*args, **kwargs)
        course_id = args[-1]['courseid']
        
        self.fields['course'].queryset = Course.objects.filter(pk = course_id)
    
# Editing the studygroup requires a slightly different form.
# It may be possible to use the same form, but not sure how yet.  Perhaps by 
# setting a default value for is_active in the init.
class StudyGroupEditForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields=['post_title', 'course', 'max_members', 'gender_specific' ,'days_available',
                'hours_available_start', 'hours_available_end', 'online_only', 'is_active']
        exclude = ['creator']
    # Need to add better labels.
    # Need to get the actual course list.
    # Need to create dropdowns.
    post_title = forms.CharField(label='Post Title', required=True, help_text='Required')
    # We want this hidden.  Will display the course details via View.
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(pk=1),
        widget = forms.HiddenInput(), required=False)
    creator = forms.ModelChoiceField(
        queryset = CustomUser.objects.filter(pk=1), 
        widget = forms.HiddenInput, required=False)
    max_members = forms.IntegerField(required=False, help_text='Optional.')
    gender_specific = forms.ChoiceField(label='Gender', widget=forms.Select, choices=MY_GENDER_CHOICES, 
                                     required=False, help_text='Optional.')
    days_available = forms.MultipleChoiceField(label='Days Available', 
                                              widget=forms.SelectMultiple, 
                                              choices=MY_DAY_CHOICES, 
                                              required=False, 
                                              help_text='Optional.')
    hours_available_start = forms.TimeInput(format='%H:%M')
    hours_available_end = forms.TimeField(#format='%H:%M',
        widget=forms.TimeInput,
        label='Hours Available End', 
        required=False,
        help_text='Optional'
    )
    online_only = forms.BooleanField(required=False, help_text='Optional.')
    is_active = forms.BooleanField(required=False, help_text='Optional')
    
    def __init__(self, *args, **kwargs):
        super(StudyGroupEditForm, self).__init__(*args, **kwargs)
        
        