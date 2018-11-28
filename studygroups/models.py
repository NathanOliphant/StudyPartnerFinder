from django.db import models
from users.models import CustomUser
import datetime
from django.core.validators import MinValueValidator
from django.utils.timezone import now as dnow
#
now = datetime.datetime.now()

MY_SEMESTER_CHOICES = (
    ('Spring', 'Spring'),
    ('Summer', 'Summer'),
    ('Fall', 'Fall')
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

MY_GENDER_CHOICES = (
         ('U', 'Undeclared'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Nonbinary')
)

# Create your models here.


# The three Choice classes are being added for phase 2.
# They do nothing at the moment.
class GenderChoice(models.Model):
    id = models.BigAutoField(primary_key = True)
    abbrev = models.CharField(max_length = 1, null = False)
    gender = models.CharField(max_length = 18, null = False)

    def __str__(self):
        return self.abbrev


class DayChoice(models.Model):
    day = models.CharField(max_length = 10, null = False)

    def __str__(self):
        return self.day


class SemesterChoice(models.Model):
    semester = models.CharField(max_length = 10, null = False)

    def __str__(self):
        return self.semester


# Subjects are used to categorize courses for search.
class Subject(models.Model):
    id = models.BigAutoField(primary_key = True)
    name = models.CharField(max_length = 256)
    description = models.CharField(max_length = 2000, null = True)
    schedule_abbreviation = models.CharField(max_length = 12, null = True)

    def __str__(self):
        return self.name


# The actual courses being searched for.  Each studygroup belongs to a specific course.
class Course(models.Model):
    id = models.BigAutoField(primary_key = True)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    cn_number = models.IntegerField(default = 0, null = True)
    class_name = models.CharField(max_length = 200)
    instructor = models.CharField(max_length = 100, default = '')
    semester = models.CharField(max_length = 6, choices = MY_SEMESTER_CHOICES)
    year = models.IntegerField(default = now.year)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return '{}'.format(self.id)


# This is used for the days that a studygroup meets.
# We will be swapping out part of this in phase 2 for days from the database
# rather than from a hard-coded enum.
class Days(models.Model):
    days_available = models.CharField(
        max_length = 255,
        choices = MY_DAY_CHOICES,
        null = True)

    def __str__(self):
        return '{}'.format(self.days_available)


# When StudyGroup created, also insert a record into StudyGroupUser.
# This will simplify gathering all StudyGroups for a user.
class StudyGroup(models.Model):
    id = models.BigAutoField(primary_key = True)
    post_title = models.CharField(max_length = 250, default = '')
    creator = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    course = models.ForeignKey(Course, on_delete = models.CASCADE, null = True)
    is_active = models.BooleanField(default = True)
    # weekday = models.BooleanField(default=True)
    # weekend = models.BooleanField(default=True)
    max_members = models.PositiveIntegerField(
        default = 1000,
        validators = [MinValueValidator(1)])
    gender_specific = models.CharField(max_length = 15, choices = MY_GENDER_CHOICES)

    days_available = models.ManyToManyField(Days)
    hours_available_start = models.TimeField(
        auto_now_add = False,
        blank = True,
        null = True,
        default = datetime.time(0, 1))
    hours_available_end = models.TimeField(
        auto_now_add = False,
        blank = True,
        null = True,
        default = datetime.time(23, 59))
    online_only = models.BooleanField(default = False)


# Since we are limiting search to only the current semester, this will be updated every
# semester.  The admin interface will need to be used for updates.
# http://127.0.0.1:8000/admin/studygroups/currentsemester/1/change/
# Substitute your hostname and port for 127.0.0.1:8000
class CurrentSemester(models.Model):
    semester = models.CharField(
        max_length = 6,
        choices = MY_SEMESTER_CHOICES,
        default = "Fall")
    year = models.PositiveIntegerField(default = now.year)


# Creators of a studygroup may block any members.  We store those blocks here.
# A blocked user no longer has access to any studygroup created by the blocker.
class BlockList(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE,
        related_name = 'blocker')
    blocked_user = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE,
        related_name = 'blockee')


# If we use ManyToMany for the user/member in StudyGroup, we can probably get rid
# of this class.  For phase 1, however, it remains.
# This contains all of the users under a studygroup.
class StudyGroupUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    studygroup = models.ForeignKey(StudyGroup, on_delete = models.CASCADE)

    def __str__(self):
        return '{}: {}, {}'.format(self.id, self.user, self.studygroup)


# Studygroup-level messaging is stored here.  We will want to create a user-level
# messaging model eventually.
class Message(models.Model):
    id = models.BigAutoField(primary_key = True)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    date = models.DateTimeField(default = dnow)
    studygroup = models.ForeignKey(StudyGroup, on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    body = models.CharField(max_length = 2000)

    def __str__(self):
        return self.title

# class Filter(models.Model):
#    id = models.BigAutoField(primary_key=True)
#    name = models.CharField(max_length=200)
#    value = models.CharField(max_length=200)

#    def __str__(self):
#        return self.name

# class StudyGroupFilter(models.Model):
#    id = models.BigAutoField(primary_key=True)
#    studygroup = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
#    filter = models.ForeignKey(Filter, on_delete=models.CASCADE)

#    def __str__(self):
#        return 'StudyGroup: {} :: Filter: {}'.format(self.studygroup, self.filter)

