from django import forms
from study.models import Subject, Course, StudyGroup, StudyGroupUser
from users.models import CustomUser


#used_his = forms.ModelMultipleChoiceField(queryset=Gun.objects.filter(user__id=1))

    #def __init__(self, user, *args, **kwargs):
    #    super(TrophiesForm, self).__init__(*args, **kwargs)
    #    self.fields['used_his'].queryset = User.objects.filter(pk = user.id)

class StudyGroupCreationForm(forms.ModelForm):
    
        
    class Meta:
        model = StudyGroup
        fields=['postTitle', 'course', 'maxMembers', 'genderSpecific' ,'daysAvailable',
                'hoursMondayStart', 'hoursMondayEnd', 'hoursTuesdayStart',
                'hoursTuesdayEnd', 'hoursWednesdayStart', 'hoursWednesdayEnd',
                'hoursThursdayStart', 'hoursThursdayEnd', 'hoursFridayStart',
                'hoursFridayEnd', 'hoursSaturdayStart', 'hoursSaturdayEnd',
                'hoursSundayStart', 'hoursSundayEnd', 'onlineOnly']
        exclude = ['creatorUserId']
    # Need to add better labels.
    # Need to get the actual course list.
    # Need to create dropdowns.
    postTitle = forms.CharField(label='Post Title', required=True, help_text='Required')
    # We want this hidden.  Will display the course details via View.
    #course = forms.CharField(label='Course')
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(pk=1),
        widget = forms.HiddenInput(), required=False)
    #isActive = forms.BooleanField(required=True, help_text='Required.')
    creatorUserId = forms.ModelChoiceField(
        queryset = CustomUser.objects.filter(pk=1), 
        widget = forms.HiddenInput, required=False)
    
    #weekday = forms.BooleanField(required=False, help_text='Optional.')
    #weekend = forms.BooleanField(required=False, help_text='Optional.')
    maxMembers = forms.IntegerField(required=False, help_text='Optional.')
    MY_GENDER_CHOICES = (
         ('U', 'Undeclared'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Nonbinary')
    )
    genderSpecific = forms.ChoiceField(label='Gender', widget=forms.Select, choices=MY_GENDER_CHOICES, 
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
    daysAvailable = forms.MultipleChoiceField(label='Days Available', 
                                              widget=forms.SelectMultiple, choices=MY_DAY_CHOICES, 
                                              required=False, help_text='Optional.')
    #monday = forms.BooleanField(required=False, help_text='Optional.')
    hoursMondayStart = forms.IntegerField(required=False, help_text='Optional.')
    hoursMondayEnd = forms.IntegerField(required=False, help_text='Optional.')
    #tuesday = forms.BooleanField(required=False, help_text='Optional.')
    hoursTuesdayStart = forms.IntegerField(required=False, help_text='Optional.')
    hoursTuesdayEnd = forms.IntegerField(required=False, help_text='Optional.')
    #wednesday = forms.BooleanField(required=False, help_text='Optional.')
    hoursWednesdayStart = forms.IntegerField(required=False, help_text='Optional.')
    hoursWednesdayEnd = forms.IntegerField(required=False, help_text='Optional.')
    #thursday = forms.BooleanField(required=False, help_text='Optional.')
    hoursThursdayStart = forms.IntegerField(required=False, help_text='Optional.')
    hoursThursdayEnd = forms.IntegerField(required=False, help_text='Optional.')
    #friday = forms.BooleanField(required=False, help_text='Optional.')
    hoursFridayStart = forms.IntegerField(required=False, help_text='Optional.')
    hoursFridayEnd = forms.IntegerField(required=False, help_text='Optional.')
    #saturday = forms.BooleanField(required=False, help_text='Optional.')
    hoursSaturdayStart = forms.IntegerField(required=False, help_text='Optional.')
    hoursSaturdayEnd = forms.IntegerField(required=False, help_text='Optional.')
    #sunday = forms.BooleanField(required=False, help_text='Optional.')
    hoursSundayStart = forms.IntegerField(required=False, help_text='Optional.')
    hoursSundayEnd = forms.IntegerField( required=False, help_text='Optional.')
    onlineOnly = forms.BooleanField(required=False, help_text='Optional.')
    
    def __init__(self, *args, **kwargs):
        super(StudyGroupCreationForm, self).__init__(*args, **kwargs)
        #with open("hello_args.txt", "w") as f:
        #    f.write('args == {}\n'.format(args))
        
        
        user_id = args[-1]['userid']
        course_id = args[-1]['courseid']
        
        
        
        #self.fields['creatorUserId'].queryset = CustomUser.objects.filter(pk = user_id)
        self.fields['course'].queryset = Course.objects.filter(pk = course_id)
    #def __init__(self, *args, **kwargs):
    #    from django.forms.widgets import HiddenInput
    #    hide_condition = kwargs.pop('id',None)
    #    super(StudyGroupCreationForm, self).__init__(*args, **kwargs)
    #    if hide_condition:
    #        self.fields['course'].widget = HiddenInput()
            # or alternately:  del self.fields['fieldname']  to remove it from the form altogether.


#form = MyModelForm(hide_condition=True)

    #def __init__(self, *args, **kwargs):
    #    super(StudyGroupCreationForm, self).__init__(*args, **kwargs)
    #    self.fields['postTitle'].label = "Post Title"
    #    self.fields['course'].label = "Course"
    #    self.fields['weekday'].label = "Weekday"
    #    self.fields['weekend'].label = "Weekend"
    
    #class Meta():
    #    model = StudyGroup
    #    fields = ('username', 'email', 'first_name', 'last_name', 'gender')
        