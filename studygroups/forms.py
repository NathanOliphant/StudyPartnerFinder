from django import forms
from studygroups.models import Course, StudyGroup
from users.models import CustomUser
#from django.core.validators import MinValueValidator

#used_his = forms.ModelMultipleChoiceField(queryset=Gun.objects.filter(user__id=1))

    #def __init__(self, user, *args, **kwargs):
    #    super(TrophiesForm, self).__init__(*args, **kwargs)
    #    self.fields['used_his'].queryset = User.objects.filter(pk = user.id)

class StudyGroupCreationForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields=['post_title', 'course', 'max_members', 'gender_specific' ,'days_available',
                'hours_available_start', 'hours_available_end', 'online_only']
        exclude = ['creator']
    # Need to add better labels.
    # Need to get the actual course list.
    # Need to create dropdowns.
    post_title = forms.CharField(label='Post Title', required=True, help_text='Required')
    # We want this hidden.  Will display the course details via View.
    #course = forms.CharField(label='Course')
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(pk=1),
        widget = forms.HiddenInput(), required=False)
    #isActive = forms.BooleanField(required=True, help_text='Required.')
    creator = forms.ModelChoiceField(
        queryset = CustomUser.objects.filter(pk=1), 
        widget = forms.HiddenInput, required=False)
    
    #weekday = forms.BooleanField(required=False, help_text='Optional.')
    #weekend = forms.BooleanField(required=False, help_text='Optional.')
    max_members = forms.IntegerField(required=False, help_text='Optional.')
    
    MY_GENDER_CHOICES = (
         ('U', 'Undeclared'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Nonbinary')
    )
    gender_specific = forms.ChoiceField(label='Gender', widget=forms.Select, choices=MY_GENDER_CHOICES, 
                                     required=False, help_text='Optional.')
    MY_DAY_CHOICES = (
         ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), 
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    )
    days_available = forms.MultipleChoiceField(label='Days Available', 
                                              widget=forms.SelectMultiple, 
                                              choices=MY_DAY_CHOICES, 
                                              required=False, 
                                              help_text='Optional.')
    hours_available_start = forms.TimeInput(format='%H:%M',
        #widget=forms.TimeField,
        #label='Hours Available Start', 
        #required=False,
        #help_text='Optional'
        )
    hours_available_end = forms.TimeField(#format='%H:%M',
        widget=forms.TimeInput,
        label='Hours Available End', 
        required=False,
        help_text='Optional'
        )
    
    online_only = forms.BooleanField(required=False, help_text='Optional.')
    
    def __init__(self, *args, **kwargs):
        super(StudyGroupCreationForm, self).__init__(*args, **kwargs)
        #user_id = args[-1]['userid']
        course_id = args[-1]['courseid']
        
        self.fields['course'].queryset = Course.objects.filter(pk = course_id)
    
class StudyGroupEditForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields=['post_title', 'course', 'max_members', 'gender_specific' ,'days_available',
                'hours_available_start', 'hours_available_end', 'online_only']
        exclude = ['creator']
    # Need to add better labels.
    # Need to get the actual course list.
    # Need to create dropdowns.
    post_title = forms.CharField(label='Post Title', required=True, help_text='Required')
    # We want this hidden.  Will display the course details via View.
    #course = forms.CharField(label='Course')
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(pk=1),
        widget = forms.HiddenInput(), required=False)
    #isActive = forms.BooleanField(required=True, help_text='Required.')
    creator = forms.ModelChoiceField(
        queryset = CustomUser.objects.filter(pk=1), 
        widget = forms.HiddenInput, required=False)
    
    #weekday = forms.BooleanField(required=False, help_text='Optional.')
    #weekend = forms.BooleanField(required=False, help_text='Optional.')
    max_members = forms.IntegerField(required=False, help_text='Optional.')
    
    MY_GENDER_CHOICES = (
         ('U', 'Undeclared'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Nonbinary')
    )
    gender_specific = forms.ChoiceField(label='Gender', widget=forms.Select, choices=MY_GENDER_CHOICES, 
                                     required=False, help_text='Optional.')
    MY_DAY_CHOICES = (
         ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), 
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    )
    days_available = forms.MultipleChoiceField(label='Days Available', 
                                              widget=forms.SelectMultiple, 
                                              choices=MY_DAY_CHOICES, 
                                              required=False, 
                                              help_text='Optional.')
    hours_available_start = forms.TimeInput(format='%H:%M',
        #widget=forms.TimeField,
        #label='Hours Available Start', 
        #required=False,
        #help_text='Optional'
        )
    hours_available_end = forms.TimeField(#format='%H:%M',
        widget=forms.TimeInput,
        label='Hours Available End', 
        required=False,
        help_text='Optional'
        )
    
    online_only = forms.BooleanField(required=False, help_text='Optional.')
    
    def __init__(self, *args, **kwargs):
        super(StudyGroupEditForm, self).__init__(*args, **kwargs)
        
        