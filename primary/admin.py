from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.
from primary.models import Address, School, Subject, Booklist, Parent_Guardian, Teacher
from primary.models import Family, Class, Student, FamilyMember
from primary.models import Parent_Address, Student_Address, StudentRegisterClass, StudentAttendsClass
from primary.models import Homework, Reports, Test, ClassName

class ClassNameAdmin(admin.ModelAdmin):
	list_display = ('class_name','class_departments')

class ClassAdmin(admin.ModelAdmin):
	list_display = ('class_name', 'teacher')
	
admin.site.register(ClassName, ClassNameAdmin)
admin.site.register(Address)
admin.site.register(School)
admin.site.register(Subject)
admin.site.register(Booklist)
admin.site.register(Parent_Guardian)
admin.site.register(Teacher)
admin.site.register(Family)
admin.site.register(Class, ClassAdmin)
admin.site.register(Student)
admin.site.register(FamilyMember)
admin.site.register(Parent_Address)
admin.site.register(Student_Address)
admin.site.register(StudentRegisterClass)
admin.site.register(StudentAttendsClass)
admin.site.register(Homework)
admin.site.register(Reports)
admin.site.register(Test)