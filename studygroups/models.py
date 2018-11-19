from django.db import models
#from django.contrib.auth.models import User as AuthUser
from users.models import CustomUser
import datetime
from django.core.validators import MinValueValidator
import datetime
now = datetime.datetime.now()

# Create your models here.
class Subject(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=2000, null=True)
    schedule_abbreviation = models.CharField(max_length=12, null=True)
    
    def __str__(self):
        return self.name
    
class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    cn_number = models.IntegerField(default=0, null=True)
    class_name = models.CharField(max_length=200)
    instructor = models.CharField(max_length=100, default='')
    
    MY_SEMESTER_CHOICES = (
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Fall', 'Fall')
    )
    semester = models.CharField(max_length=6, choices=MY_SEMESTER_CHOICES)
    
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
    year = models.IntegerField(default=2018, choices=MY_YEAR_CHOICES)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        #return '{}, {} {}, {}, {}'.format(self.className, self.semester, self.year, self.instructor, self.cNNumber)
        return '{}'.format(self.id)
    
class Days(models.Model):
    MY_DAY_CHOICES = (
         ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), 
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    )
    days_available = models.CharField(max_length=255, choices=MY_DAY_CHOICES, null=True)
    
    def __str__(self):
        return '{}'.format(self.days_available)
    
# When StudyGroup created, also insert a record into StudyGroupUser.
# This will simplify gathering all StudyGroups for a user.
class StudyGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    post_title = models.CharField(max_length=250, default='')
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    #weekday = models.BooleanField(default=True)
    #weekend = models.BooleanField(default=True)
    max_members = models.PositiveIntegerField(default=1000, validators=[MinValueValidator(1)])
    MY_GENDER_CHOICES = (
         ('U', 'Undeclared'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Nonbinary')
    )
    gender_specific = models.CharField(max_length=15, choices=MY_GENDER_CHOICES)
    
    #MY_DAY_CHOICES = (
    #     ('Monday', 'Monday'),
    #    ('Tuesday', 'Tuesday'),
    #    ('Wednesday', 'Wednesday'),
    #    ('Thursday', 'Thursday'), 
    #    ('Friday', 'Friday'),
    #    ('Saturday', 'Saturday'),
    #    ('Sunday', 'Sunday')
    #)
    days_available = models.ManyToManyField(Days)
    hours_available_start = models.TimeField(auto_now_add=False, blank=True, null=True, default=datetime.time(0, 1))
    hours_available_end = models.TimeField(auto_now_add=False, blank=True, null=True, default=datetime.time(23, 59))
    online_only = models.BooleanField(default = False)
    
    #def __str__(self):
    #    return '{}, {}, {}'.format(self.id, self.creatorUserId, self.course)
MY_SEMESTER_CHOICES = (
         ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
    )  
class CurrentSemester(models.Model):
    semester = models.CharField(max_length=6, choices=MY_SEMESTER_CHOICES, default="Fall")
    year = models.PositiveIntegerField(default = now.year)
    
class BlockList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blocker')
    blocked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blockee')

class StudyGroupUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    studygroup = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    def __str__(self):
        return '{}: {}, {}'.format(self.id, self.user, self.studygroup)
    
class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField()
    studygroup = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=2000)
    
    def __str__(self):
        return self.title
    
class Filter(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class StudyGroupFilter(models.Model):
    id = models.BigAutoField(primary_key=True)
    studygroup = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'StudyGroup: {} :: Filter: {}'.format(self.studygroup, self.filter)
    
    
    
