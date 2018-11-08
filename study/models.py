from django.db import models
from django.contrib.auth.models import User as AuthUser
from users.models import CustomUser

# Create your models here.

# Need to change User so that it either extends AuthUser,
# or contains items missing from AuthUser, and use the two together.
# May switch to UserProfile????
#AuthUser:
# CREATE TABLE IF NOT EXISTS "auth_user" (
# "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
# "password" varchar(128) NOT NULL, 
# "last_login" datetime NULL, 
# "is_superuser" bool NOT NULL, 
# "username" varchar(150) NOT NULL UNIQUE, 
# "first_name" varchar(30) NOT NULL, 
# "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, 
# "is_active" bool NOT NULL, 
# "date_joined" datetime NOT NULL, 
# "last_name" varchar(150) NOT NULL);

# Need username + college to be unique!!!!
# class User(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     username = models.CharField(max_length=200)
#     firstName = models.CharField(max_length=200)
#     lastName = models.CharField(max_length=200)
#     college = models.CharField(default='humboldt.edu', max_length=200)
#     gender = models.CharField(max_length=1)
#     password = models.CharField(max_length=100)
#     isVerified = models.BooleanField(default=False)
#     verificationCode = models.CharField(max_length=200)
#     verificationDate = models.DateTimeField('date verified')
#     hasAcceptedTOS = models.BooleanField(default=False)
#     creationDate = models.DateTimeField('date created')
#     isAdminUser = models.BooleanField(default=False)
#     isActive = models.BooleanField(default=False)
#     
#     def __str__(self):
#         return self.username

#class UserProfile(models.Model):
#    user_id = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
#    college = models.CharField(default='humboldt.edu', max_length=200)
#    gender = models.CharField(max_length=1)
#    isVerified = models.BooleanField(default=False)
#    verificationCode = models.CharField(max_length=200)
#    verificationDate = models.DateTimeField('date verified')
#    hasAcceptedTOS = models.BooleanField(default=False)

class Subject(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=2000, null=True)
    scheduleAbbreviation = models.CharField(max_length=12, null=True)
    
    def __str__(self):
        return self.name
    
class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    cNNumber = models.IntegerField(default=0, null=True)
    className = models.CharField(max_length=200)
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
    isActive = models.BooleanField(default=True)
    
    def __str__(self):
        #return '{}, {} {}, {}, {}'.format(self.className, self.semester, self.year, self.instructor, self.cNNumber)
        return '{}'.format(self.id)
    
# When StudyGroup created, also insert a record into StudyGroupUser.
# This will simplify gathering all StudyGroups for a user.
class StudyGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    postTitle = models.CharField(max_length=250, default='')
    creatorUserId = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    isActive = models.BooleanField(default=True)
    #weekday = models.BooleanField(default=True)
    #weekend = models.BooleanField(default=True)
    maxMembers = models.IntegerField(default=1000)
    MY_GENDER_CHOICES = (
         ('U', 'Undeclared'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Nonbinary')
    )
    genderSpecific = models.CharField(max_length=15, choices=MY_GENDER_CHOICES)
    
    MY_DAY_CHOICES = (
         ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), 
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    )
    daysAvailable = models.CharField(default='', max_length=255)
    
    #monday = models.BooleanField(default=True)
    hoursMondayStart = models.IntegerField(default = 0)
    hoursMondayEnd = models.IntegerField(default = 2359)
    #tuesday = models.BooleanField(default=True)
    hoursTuesdayStart = models.IntegerField(default = 0)
    hoursTuesdayEnd = models.IntegerField(default = 2359)
    #wednesday = models.BooleanField(default=True)
    hoursWednesdayStart = models.IntegerField(default = 0)
    hoursWednesdayEnd = models.IntegerField(default = 2359)
    #thursday = models.BooleanField(default=True)
    hoursThursdayStart = models.IntegerField(default = 0)
    hoursThursdayEnd = models.IntegerField(default = 2359)
    #friday = models.BooleanField(default=True)
    hoursFridayStart = models.IntegerField(default = 0)
    hoursFridayEnd = models.IntegerField(default = 2359)
    #saturday = models.BooleanField(default=True)
    hoursSaturdayStart = models.IntegerField(default = 0)
    hoursSaturdayEnd = models.IntegerField(default = 2359)
    #sunday = models.BooleanField(default=True)
    hoursSundayStart = models.IntegerField(default = 0)
    hoursSundayEnd = models.IntegerField(default = 2359)
    onlineOnly = models.BooleanField(default = False)
    
    def __str__(self):
        return '{}, {}, {}'.format(self.id, self.creatorUserId, self.course)
    
class BlockList(models.Model):
    userId = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blocker')
    blockedUserId = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blockee')

class StudyGroupUser(models.Model):
    userId = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    studyGroupId = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    def __str__(self):
        return '{}: {}, {}'.format(self.id, self.userId, self.studyGroupId)
    
class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    userId = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField()
    studyGroupId = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
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
    studyGroupId = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    filterId = models.ForeignKey(Filter, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'StudyGroup: {} :: Filter: {}'.format(self.studyGroupId, self.filterId)


class SystemLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    userId = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField()
    service = models.CharField(max_length=200)
    data = models.CharField(max_length=2000)
    
    
    