from django.contrib import admin

from primary.models import *


class ClassNameAdmin(admin.ModelAdmin):
    list_display = ['class_name',]


class ClassAdmin(admin.ModelAdmin):
    list_display = ['class_name', 'teacher',]


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
