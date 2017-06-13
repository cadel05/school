from __future__ import unicode_literals

from django.db import models
import datetime
from datetime import date
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.db.models import signals
from django.dispatch import dispatcher
from django.utils import timezone


# Create your models here.

class Address(models.Model):
    street = models.CharField(max_length=254)
    town = models.CharField(max_length=254, null=True, blank=True)
    city = models.CharField(max_length=254, null=True, blank=True)
    country = models.CharField(max_length=100, default='Trinidad')
    phone = models.CharField(max_length=12, null=True, blank=True)

    def __unicode__(self):
        return self.street


TYPE = (
    ('', ''),
    ('P', 'Primary School'),
    ('S', 'Secondary School'),
)


class School(models.Model):
    type = models.CharField(max_length=20, choices=TYPE, default='')
    address = models.OneToOneField(Address)
    name = models.CharField(max_length=254)
    principal = models.CharField(max_length=254)
    email = models.CharField(max_length=50)
    fax = models.CharField(max_length=12, null=True, blank=True)

    def __unicode__(self):
        return self.name


# Recently Added
TERM = (
    ('1', 'Term 1'),
    ('2', 'Term 2'),
    ('3', 'Term 3'),
)


class AcademicYear(models.Model):
    school = models.ForeignKey(School, default=1)
    openDate = models.DateTimeField(default=timezone.now)
    closedDate = models.DateTimeField(default=timezone.now)
    term = models.CharField(max_length=10, choices=TERM, default='1')


class Subject(models.Model):
    subject = models.CharField(max_length=75)

    def __unicode__(self):
        return self.subject


class Booklist(models.Model):
    textbook = models.CharField(max_length=254, blank=True, null=True)
    bluepens = models.IntegerField(null=True, blank=True, default=0)
    blackpens = models.IntegerField(null=True, blank=True, default=0)
    redpens = models.IntegerField(null=True, blank=True, default=0)
    pencils = models.IntegerField(null=True, blank=True, default=0)
    copybooks = models.IntegerField(null=True, blank=True, default=0)
    gluestick = models.IntegerField(null=True, blank=True, default=0)
    ruler = models.BooleanField(default=False)
    geometryset = models.BooleanField(default=False)
    lettersizepaper = models.IntegerField(null=True, blank=True)
    dressuniform = models.CharField(max_length=254, blank=True, null=True)
    PEuniform = models.CharField(max_length=254, blank=True, null=True)
    subject = models.ForeignKey(Subject)

    def __unicode__(self):
        return self.textbook


SEX = (
    ('M', 'Male'),
    ('F', 'Female'),
)
RELATIONSHIP = (
    ('M', 'Mother'),
    ('F', 'Father'),
    ('B', 'Brother'),
    ('S', 'Sister'),
    ('A', 'Aunt'),
    ('U', 'Uncle'),
    ('G', 'Grand Parent'),
    ('C', 'Cousin'),
    ('L', 'Legal Guardian')
)


class Parent_Guardian(models.Model):
    gender = models.CharField(max_length=1, choices=SEX)
    parent = models.OneToOneField(User, on_delete=models.CASCADE)
    cell_phone = models.CharField(max_length=12)
    cell_phone = models.CharField(max_length=12)
    personal_email = models.CharField(max_length=50)
    personal_fax = models.CharField(max_length=12, blank=True, null=True)
    work_name = models.CharField(max_length=150, blank=True, null=True)
    work_phone = models.CharField(max_length=12, blank=True, null=True)
    relationship = models.CharField(max_length=5, choices=RELATIONSHIP)
    address = models.ManyToManyField(Address, through='Parent_Address')

    def __unicode__(self):
        return unicode(self.parent)


class Teacher(models.Model):
    gender = models.CharField(max_length=1, choices=SEX)
    teacher = models.OneToOneField(User)
    cell_phone = models.CharField(max_length=12, blank=True, null=True)
    personal_email = models.CharField(max_length=50)
    personal_fax = models.CharField(max_length=12, blank=True, null=True)
    head_teacher = models.BooleanField(default=False)
    school = models.ForeignKey(School)

    def __unicode__(self):
        return unicode(self.teacher)


CLASSES = (
    ('N', 'NURSERY'),
    ('INFANTS 1', 'INFANTS 1'),
    ('INFANTS 2', 'INFANTS 2'),
    ('STD 1', 'STANDARD 1'),
    ('STD 2', 'STANDARD 2'),
    ('STD 3', 'STANDARD 3'),
    ('STD 4', 'STANDARD 4'),
    ('STD 5', 'STANDARD 5'),
    ('FORM 1', 'FORM 1'),
    ('FORM 2', 'FORM 2'),
    ('FORM 3', 'FORM 3'),
    ('FORM 4', 'FORM 4'),
    ('FORM 5', 'FORM 5'),
    ('FORM 6', 'FORM 6'),
)


DEPARTMENTS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
)


class ClassName(models.Model):
    class_name = models.CharField(max_length=100, choices = CLASSES)
    class_departments = models.CharField(max_length=10, choices=DEPARTMENTS, blank=True, null=True)

    def __unicode__(self):
        return '%s - %s' % (self.class_name, self.class_departments)


class Class(models.Model):
    subject = models.ManyToManyField(Subject)
    teacher = models.ForeignKey(Teacher)
    class_name = models.ForeignKey(ClassName)
    classDaysandTime = models.CharField(max_length=255,
                                        help_text='Monday - Wednesday 2pm -3pm, Friday 10:00 am - 11:00 am')
    class_room = models.CharField(max_length=50, default='Room Standard 1 A', null=True, blank=True)

    class Meta:
        unique_together = (
            (
                'teacher', 'classDaysandTime',
            )
        )

    def __str__(self):
        return '%s' % self.class_name.class_name


class Family(models.Model):
    family_head = models.ForeignKey(Parent_Guardian)
    family_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.family_name


class Student(models.Model):
    gender = models.CharField(max_length=1, choices=SEX)
    dob = models.DateField()
    allergies = models.CharField(max_length=254, null=True, blank=True)
    medical_conditions = models.CharField(max_length=254, null=True, blank=True)
    religious_belief = models.CharField(max_length=254, null=True, blank=True)
    email = models.CharField(max_length=254, null=True, blank=True)
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    parent = models.ManyToManyField(Parent_Guardian)
    address = models.ManyToManyField(Address, through='Student_Address')
    attendance = models.ManyToManyField(Class, through='StudentAttendsClass')
    class_registered = models.ManyToManyField(Class, through='StudentRegisterClass', related_name='registers')

    def __unicode__(self):
        return unicode(self.student)


class FamilyMember(models.Model):
    family = models.ForeignKey(Family)
    guardian = models.BooleanField()
    parent = models.ForeignKey(Parent_Guardian)
    student = models.ForeignKey(Student)


class Parent_Address(models.Model):
    parent = models.ForeignKey(Parent_Guardian)
    address = models.ForeignKey(Address)
    date_address_from = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.parent)


class Student_Address(models.Model):
    student = models.ForeignKey(Student)
    address = models.ForeignKey(Address)
    date_from = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.student)


class StudentRegisterClass(models.Model):
    student = models.ForeignKey(Student)
    class_name = models.ForeignKey(Class)
    date = models.DateField(default=date.today)
    comments = models.CharField(max_length=200, blank=True, null=True)


class StudentAttendsClass(models.Model):
    student = models.ForeignKey(Student)
    class_name = models.ForeignKey(Class)
    date = models.DateField(default=date.today)
    attended = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.student)


class Homework(models.Model):
    student = models.ForeignKey(Student)
    class_name = models.ForeignKey(Class)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    grade = models.CharField(max_length=40, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.class_name


CATEGORY = (
    ('M', 'PTA'),
    ('D', 'Discipline'),
    ('E', 'Event'),
    ('C', 'Closure'),
    ('A', 'Absentism'),
)


class Reports(models.Model):
    student = models.ForeignKey(Student)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    category = models.CharField(max_length=2, choices=CATEGORY)
    teachers_comments = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.category


TEST_TYPE = (
    ('M', 'Multiple Choice'),
    ('S', 'Short Written Answers'),
    ('E', 'Essay Type Answers'),
    ('O', 'Oral'),
    ('L', 'Lab'),
)


class Test(models.Model):
    type = models.CharField(max_length=1, choices=TEST_TYPE)
    topic = models.CharField(max_length=254)
    preparation_material = models.TextField(null=True, blank=True)
    date_set = models.DateField()
    date_corrected = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=50)
    comments = models.TextField(null=True, blank=True)
    duration = models.CharField(max_length=50, default='30 minutes')
    class_name = models.ForeignKey(Class)
    student = models.ForeignKey(Student)

    def __unicode__(self):
        return self.type
