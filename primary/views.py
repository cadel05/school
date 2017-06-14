from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render

import json

import datetime

from django.contrib.auth.models import Group

from .models import School, Address, Teacher, Parent_Guardian, Parent_Address, Student, Student_Address, Subject, Class, \
    StudentAttendsClass
from .models import StudentRegisterClass, ClassName

from .forms import CreateSchoolForm, CreateTeacherForm, CreateParentForm, CreateRegistrationForm, UpdateStudentForm

from .forms import StudentModelForm, UserModelForm, AddressModelForm, ParentModelForm, TeacherModelForm, \
    SubjectModelForm, ClassModelForm
from .forms import StudentSearchForm, SchoolModelForm, ClassNameForm, ClassNameModelForm, SelectSubjectsForm

from django.views import generic
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.views.generic import ListView, CreateView

from django.db.models import Max

from django.utils import timezone

import logging

from django.core import serializers

"""
#############################Group name Administrators must be set they have the power to add students, etc, view all reports
#############################New Group of Teachers need to be created, Parents, Students and School Staff need to be created
"""


##################################
@login_required
def profile_teacher_update(request, teacher_id):
    if request.method == "POST":

        userform = UserModelForm(request.POST)
        teacherform = TeacherModelForm(request.POST)

        if userform.is_valid() and teacherform.is_valid():

            first_name = userform.cleaned_data['first_name']
            last_name = userform.cleaned_data['last_name']
            email = userform.cleaned_data['email']

            cell = teacherform.cleaned_data['cell_phone']
            gender = teacherform.cleaned_data['gender']

            fax = teacherform.cleaned_data['personal_fax']
            personal_email = teacherform.cleaned_data['personal_email']

            if (first_name and last_name and email and gender):
                teacher = Teacher.objects.get(id=teacher_id)
                print "teacher"
                print teacher
                teacher.cell_phone = cell
                teacher.gender = gender
                teacher.personal_fax = fax
                teacher.personal_email = personal_email
                teacher.save()

                user_id = Teacher.objects.filter(id=teacher_id).values('teacher')
                user = User.objects.get(id=user_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()

                # messages.success('The Student Profile was successfully updated.')
        else:
            # message.error('Student was not updated')
            print 'error was not updated'
            print userform.errors

        return HttpResponseRedirect('/')
    else:
        all = Teacher.objects.get(id=teacher_id)
        print all
        user = Teacher.objects.filter(id=teacher_id).values_list('teacher')
        first = User.objects.get(id=user)
        teacherform = TeacherModelForm(instance=all)
        userform = UserModelForm(instance=first)

        return render(request, 'teacher/teacher_update_form.html', {
            'userform': userform,
            'teacherform': teacherform,
            'all': all,
            'user': first
        })


###############################
"""
def student_subject_register(request):
	if request.method == 'POST':
		student = request.POST['student']
		class_id = request.POST.getlist('class_id')
		if student and class_id:
			class_id = request.POST.getlist('class_id')
			st = Student.objects.get(id=student)
			for c in class_id :
				if c:
					classes = Class.objects.get(id = c)
					student_register = StudentRegisterClass(student = st, class_name = classes)
					student_register.save()
			return HttpResponseRedirect('/')
		else:
			if(student):
				subject = Subject.objects.all()
				classes = Class.objects.filter(subject__in = subject)
				student = Student.objects.filter(id = student)
				
				school = School.objects.all()
				current_year = timezone.now().year
				#register = StudentRegisterClass.objects.filter(student = student, academic_year__openDate__year = current_year)
				register = StudentRegisterClass.objects.filter(student = student)
				if (not register):
					current_year = current_year - 1
					#register = StudentRegisterClass.objects.filter(student = student, academic_year__openDate__year = current_year)
				form = ClassNameForm()
				subjects_form = ClassNameModelForm()
			return render(request, 'class/student_registration.html', 
				{
					'subject' : subject,
					'classes' : classes,
					'student' : student,
				
					'register' : register,
					'school' : school,
					'form' : form,
					'subjects_form' : subjects_form,
				})
	else:
		print "wtf"
		return HttpResponseRedirect('/')
		
"""
###############################
"""
Potential Issue to Test for: Classes Model, Classes can exist and no longer available,
Only display classes that have been registered for academic year
"""


def classRegistration(request, student_id, user_id):

    if request.method == 'POST':
        classform = ClassNameForm(request.POST)
        subjectsform = ClassNameModelForm(request.POST)

        if classform.is_valid() or subjectsform.is_valid():

            select_subjects = classform.cleaned_data['select_subjects']
            select_subjects = subjectsform.cleaned_data['select_subjects']

            if select_subjects == 'True':

                class_name = subjectsform.cleaned_data['class_name']

                class_name = ClassName.objects.filter(class_name=class_name)

                classes = Class.objects.filter(class_name__in=class_name).order_by('subject')

                form = SelectSubjectsForm(classes=classes)
                return render(request, 'class/select_subjects_form.html',
                              {
                                  'form': form,
                                  'classes': classes,
                                  'student_id': student_id,
                              }
                              )

            else:
                print "class"
                print select_subjects
                class_name = classform.cleaned_data['class_name']
                classes = Class.objects.filter(class_name=class_name)
                print classes

        studentForm = StudentSearchForm()
        return render(request, 'class/student_search.html',
                      {
                          'form': StudentSearchForm,
                      }
                      )
    else:
        if 'class' in request.GET and request.GET['class'] is not None:
            try:
                class_name = ClassName.objects.get(pk=int(request.GET['class']))
                classes = Class.objects.filter(class_name=class_name)
                l = [[", ".join([s.subject for s in x.subject.all()]), x.teacher.teacher.get_full_name(),
                      x.class_name.class_name, x.classDaysandTime, x.id] for x in classes]
                return HttpResponse(json.dumps(l))
            except Exception as e:
                logging.error(e)
                return HttpResponse(e)
        if 'reg_class' in request.GET and request.GET['reg_class'] is not None:
            reg_class_ids = list(request.GET['reg_class'])
            for rci in reg_class_ids:
                try:
                    class_to_reg = Class.objects.get(pk=rci)
                    student = Student.objects.get(pk=student_id)
                    src = StudentRegisterClass(student=student, class_name=class_to_reg)
                    src.save()
                except:
                    pass
            return HttpResponse('OK')
        if 'rc_del' in request.GET and request.GET['rc_del'] is not None:
            try:
                src = StudentRegisterClass.objects.get(pk=request.GET['rc_del'])
                src.delete()
                return HttpResponse('OK')
            except Exception as e:
                logging.error(e)
                return HttpResponse('Err', status=500)
        if (student_id):
            subject = Subject.objects.all()
            classes = Class.objects.filter(subject__in=subject)
            student = Student.objects.filter(id=student_id)
            user = User.objects.filter(id=user_id)
            school = School.objects.all()
            current_year = timezone.now().year
            reg_classes = StudentRegisterClass.objects.filter(student=student[0])
            # register = StudentRegisterClass.objects.filter(student = student, academic_year__openDate__year = current_year)
            register = StudentRegisterClass.objects.filter(student=student)
            if (not register):
                current_year = current_year - 1
            # register = StudentRegisterClass.objects.filter(student = student)
            print register
            form = ClassNameForm()
            subjects_form = ClassNameModelForm()
            return render(request, 'class/student_registration.html',
                          {
                              'subject': subject,
                              'classes': classes,
                              'student': student,
                              'user': user,
                              'register': register,
                              'reg_classes': reg_classes,
                              'school': school,
                              'form': form,
                              'subjects_form': subjects_form,
                          })
        if (not student_id):
            studentForm = StudentSearchForm()
            return render(request, 'class/student_search.html',
                          {
                              'form': StudentSearchForm,
                          }
                          )


#############################
##Should be limited to Administrators and Teacher Groups
@login_required
def searchStudent(request):
    if request.method == 'POST':
        studentForm = StudentSearchForm(request.POST)
        if studentForm.is_valid():
            first_name = studentForm.cleaned_data['first_name']
            last_name = studentForm.cleaned_data['last_name']
            if (first_name and last_name):
                user = User.objects.filter(first_name__icontains=first_name, last_name__icontains=last_name)
                student = Student.objects.filter(student__in=user)

            if (first_name and not last_name):
                user = User.objects.filter(first_name__icontains=first_name)
                student = Student.objects.filter(student__in=user)

            if (not first_name and last_name):
                user = User.objects.filter(last_name__icontains=last_name)
                student = Student.objects.filter(student__in=user)

            if (not first_name and not last_name):
                user = User.objects.all()
                student = Student.objects.filter(student__in=user)

            return render(request, 'class/student_search_details.html',
                          {
                              'user': user,
                              'student': student,

                          }
                          )
    else:
        studentForm = StudentSearchForm()
        return render(request, 'class/student_search.html',
                      {
                          'form': studentForm,
                      }
                      )


#########################################################
class ClassCreateView(CreateView):
    model = Class
    form_class = ClassModelForm
    template_name = 'class/class_create.html'

    def get_success_url(self):
        return reverse('list_class')


###################
class ClassUpdateView(UpdateView):
    model = Subject
    form_class = ClassModelForm
    template_name = 'class/class_update_form.html'

    def get_object(self, queryset=None):
        obj = Class.objects.get(id=self.kwargs['pk'])
        return obj

    def get_success_url(self):
        return reverse('list_class')


###################
class ClassListView(ListView):
    model = Class
    template_name = 'class/class_list.html'


###############################
class SubjectCreateView(CreateView):
    model = Subject
    fields = ['subject']
    template_name = 'school/subject_create.html'

    def get_success_url(self):
        return reverse('list_subject')


###################
class SubjectListView(ListView):
    model = Subject
    template_name = 'school/subject_list.html'


###################
class SubjectUpdateView(UpdateView):
    model = Subject
    fields = [
        'subject'
    ]
    template_name = 'school/subject_update_form.html'

    def get_success_url(self):
        return reverse('list_subject')


###############################

class TeacherListView(ListView):
    model = Teacher
    template_name = 'teacher/teacher_list.html'


###################
class SchoolUpdateView(UpdateView):
    model = School
    fields = [
        'name'
    ]
    template_name = 'school/school_update_form.html'

    def get_success_url(self):
        return reverse('list_school')


class SchoolListView(ListView):
    model = School
    template_name = 'school/school_list.html'


################
@login_required
def school_address_update(request, address_id, school_id):
    if request.method == 'POST':
        addressForm = AddressModelForm(request.POST)
        if addressForm.is_valid():
            street = addressForm.cleaned_data['street']
            city = addressForm.cleaned_data['city']
            town = addressForm.cleaned_data['town']
            country = addressForm.cleaned_data['country']
            if (street and country):
                address = Address.objects.get(id=address_id)
                address.street = street
                address.city = city
                address.country = country
                address.town = town
                address.save()

        else:
            addressForm.errors
        return HttpResponseRedirect('/')
    else:
        all = School.objects.filter(id=school_id)
        address = Address.objects.get(id=address_id)
        print "address"
        print address
        addressForm = AddressModelForm(instance=address)
        return render(request, 'school/school_address_update.html', {'all': all, 'addressForm': addressForm})


################
class StudentListView(generic.ListView):
    model = Student


"""	
####List Student Profile Details	
## Need to create one for teachers to list for depending on class taught
"""


@login_required
def profile_student(request):
    print request.user.groups.all()
    if (request.user.groups.filter(name='Administrators')):
        all = Student.objects.all()
    if (request.user.groups.filter(name='Parents')):
        parent = Parent_Guardian.objects.filter(parent=request.user)
        all = Student.objects.filter(parent=parent)
    if (request.user.groups.filter(name='Teachers')):
        print "do something"
    if (request.user.groups.filter(name='Students')):
        print "all in here"
        all = Student.objects.filter(student=request.user)
    return render(request, 'primary/view_student_profile.html', {'all': all})


"""
"""


@login_required
def profile_student_details(request, student_id):
    if (request.user.groups.filter(name='Administrators')):
        all = Student.objects.filter(id=student_id)
    if (request.user.groups.filter(name='Parents')):
        parent = Parent_Guardian.objects.filter(parent=request.user)
        all = Student.objects.filter(parent=parent)
    if (request.user.groups.filter(name='Teachers')):
        print "do something"
    if (request.user.groups.filter(name='Students')):
        all = Student.objects.filter(student=request.user)
    return render(request, 'primary/view_student_detail.html', {'all': all})


"""
"""


# Same Details for parents and student
@login_required
def profile_parent_details(request, parent_id):
    if (request.user.groups.filter(name='Administrators')):
        all = Parent_Guardian.objects.filter(id=parent_id)
    else:
        all = Parent_Guardian.objects.filter(id=parent_id)
    return render(request, 'primary/view_parent_detail.html', {'all': all})


"""
"""


@login_required
def profile_student_update(request, student_id):
    if request.method == "POST":

        userform = UserModelForm(request.POST)
        studentform = StudentModelForm(request.POST)

        if userform.is_valid() and studentform.is_valid():

            first_name = userform.cleaned_data['first_name']
            last_name = userform.cleaned_data['last_name']
            email = userform.cleaned_data['email']

            dob = studentform.cleaned_data['dob']
            gender = studentform.cleaned_data['gender']
            allergies = studentform.cleaned_data['allergies']
            medical_conditions = studentform.cleaned_data['medical_conditions']
            religious_belief = studentform.cleaned_data['religious_belief']

            if (first_name and last_name and email):
                print "thrid"
                student = Student.objects.get(id=student_id)
                student.dob = dob
                student.allergies = allergies
                student.medical_conditions = medical_conditions
                student.religious_belief = religious_belief
                student.gender = gender
                student.save()

                user_id = Student.objects.filter(id=student_id).values('student')
                user = User.objects.get(id=user_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()

                # messages.success('The Student Profile was successfully updated.')
        else:
            # message.error('Student was not updated')
            print 'error was not updated'
            print userform.errors

        return HttpResponseRedirect('/')
    else:
        ###Check to see if user from admin group else use request.user
        if (not request.user.groups.filter(name='Administrators')):
            student_id = request.user
        all = Student.objects.get(id=student_id)
        user = Student.objects.filter(id=student_id).values_list('student')
        first = User.objects.get(id=user)
        studentform = StudentModelForm(instance=all)
        userform = UserModelForm(instance=first)

        return render(request, 'primary/student_update_form.html', {
            'userform': userform,
            'studentform': studentform,
            'all': all,
            'user': first
        })


"""
"""


@login_required
def profile_parent_update(request, parent_id):
    if request.method == "POST":

        userform = UserModelForm(request.POST)
        parentform = ParentModelForm(request.POST)

        if userform.is_valid() and parentform.is_valid():

            first_name = userform.cleaned_data['first_name']
            last_name = userform.cleaned_data['last_name']
            email = userform.cleaned_data['email']

            cell = parentform.cleaned_data['cell_phone']
            gender = parentform.cleaned_data['gender']
            work_name = parentform.cleaned_data['work_name']
            work_phone = parentform.cleaned_data['work_phone']
            relationship = parentform.cleaned_data['relationship']

            if (first_name and last_name and email and cell and relationship):
                print "thrid"
                parent = Parent_Guardian.objects.get(id=parent_id)
                parent.cell = cell
                parent.gender = gender
                parent.work_name = work_name
                parent.work_phone = work_phone
                parent.relationship = relationship
                parent.save()

                user_id = Parent_Guardian.objects.filter(id=parent_id).values('parent')
                user = User.objects.get(id=user_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()

                # messages.success('The Student Profile was successfully updated.')
        else:
            # message.error('Student was not updated')
            print 'error was not updated'
            print userform.errors

        return HttpResponseRedirect('/')
    else:
        all = Parent_Guardian.objects.get(id=parent_id)
        print all
        user = Parent_Guardian.objects.filter(id=parent_id).values_list('parent')
        first = User.objects.get(id=user)
        parentform = ParentModelForm(instance=all)
        userform = UserModelForm(instance=first)

        return render(request, 'primary/parent_update_form.html', {
            'userform': userform,
            'parentform': parentform,
            'all': all,
            'user': first
        })


"""
"""


@login_required
def profile_student_address_update(request, student_id, address_id):
    if request.method == 'POST':
        addressForm = AddressModelForm(request.POST)
        if addressForm.is_valid():
            street = addressForm.cleaned_data['street']
            city = addressForm.cleaned_data['city']
            town = addressForm.cleaned_data['town']
            country = addressForm.cleaned_data['country']
            if (street and country):
                user = Student.objects.filter(id=student_id).values_list('student')
                address = Address.objects.get(id=address_id)
                address.street = street
                address.city = city
                address.country = country
                address.town = town
                address.save()

        else:
            addressForm.errors
        return HttpResponseRedirect('/')
    else:
        all = Student.objects.filter(id=student_id)
        address = Address.objects.get(id=address_id)
        print "address"
        print address
        addressForm = AddressModelForm(instance=address)
        return render(request, 'primary/view_student_address_update.html', {'all': all, 'addressForm': addressForm})


"""
"""


##profile parent address update
@login_required
def profile_parent_address_update(request, parent_id, address_id):
    if request.method == 'POST':
        addressForm = AddressModelForm(request.POST)
        if addressForm.is_valid():
            street = addressForm.cleaned_data['street']
            city = addressForm.cleaned_data['city']
            town = addressForm.cleaned_data['town']
            country = addressForm.cleaned_data['country']
            if (street and country):
                user = Parent_Guardian.objects.filter(id=parent_id).values_list('parent')
                address = Address.objects.get(id=address_id)
                address.street = street
                address.city = city
                address.country = country
                address.town = town
                address.save()

        else:
            addressForm.errors
        return HttpResponseRedirect('/')
    else:
        parent = Parent_Guardian.objects.filter(id=parent_id)
        address = Address.objects.get(id=address_id)
        print "address"
        print address
        addressForm = AddressModelForm(instance=address)
        return render(request, 'primary/view_student_address_update.html',
                      {'parent': parent, 'addressForm': addressForm})


"""
"""


@login_required
def create_parent(request):
    if request.method == "POST":
        form = CreateParentForm(request.POST)

        if form.is_valid():
            home_street = form.cleaned_data['home_street']
            home_town = form.cleaned_data['home_town']
            home_city = form.cleaned_data['home_city']
            home_country = form.cleaned_data['home_country']
            home_phone = form.cleaned_data['home_phone']

            work_name = form.cleaned_data['work_name']
            work_phone = form.cleaned_data['work_phone']

            first = form.cleaned_data['first_name']
            last = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']
            cell = form.cleaned_data['phone']
            email = form.cleaned_data['email']

            fax = form.cleaned_data['fax']

            if (
                                                                        first and last and gender and cell and username and password and email and home_street and home_town and home_city and home_country and
                                home_phone and work_name and work_phone):

                home_address = Address(street=home_street, town=home_town, city=home_city, country=home_country,
                                       phone=home_phone)
                home_address.save()
                home_address_id = home_address

                user = User(username=username, first_name=first, last_name=last, password=password, email=email)
                user.save()
                user_id = user
                parent = Parent_Guardian(gender=gender, personal_email=email, parent=user_id, cell_phone=cell,
                                         personal_fax=fax,
                                         work_phone=work_phone, work_name=work_name, address=home_address)
                parent.save()
            else:
                print "error"
                # redirect to a new URL:
            return HttpResponseRedirect('/')

            # If this is a GET (or any other method) create the default form.
    else:

        form = CreateParentForm()

    return render(request, 'create_parent.html', {'form': form})


"""
"""


# Need to set random Password, email user username and password, and assign to group
# Email Errors
# set up messages - > success, error pages
#
@login_required
def create_student(request):
    if request.method == "POST":

        form = CreateRegistrationForm(request.POST)

        if form.is_valid():

            student_first = form.cleaned_data['student_first_name']
            student_last = form.cleaned_data['student_last_name']
            student_gender = form.cleaned_data['student_gender']
            student_email = form.cleaned_data['student_email']
            student_dob = form.cleaned_data['student_dob']
            student_medical = form.cleaned_data['student_medical_conditions']
            student_religious = form.cleaned_data['student_religious_belief']
            student_allergies = form.cleaned_data['student_allergies']
            student_home_street = form.cleaned_data['student_home_street']
            student_home_town = form.cleaned_data['student_home_town']
            student_home_city = form.cleaned_data['student_home_city']
            student_home_country = form.cleaned_data['student_home_country']
            student_home_phone = form.cleaned_data['student_home_phone']
            # father
            father_home_street = form.cleaned_data['father_home_street']
            father_home_town = form.cleaned_data['father_home_town']
            father_home_city = form.cleaned_data['father_home_city']
            father_home_country = form.cleaned_data['father_home_country']
            father_home_phone = form.cleaned_data['father_home_phone']

            father_work_name = form.cleaned_data['father_work_name']
            father_work_phone = form.cleaned_data['father_work_phone']

            father_first = form.cleaned_data['father_first_name']
            father_last = form.cleaned_data['father_last_name']
            father_gender = form.cleaned_data['father_gender']
            father_cell = form.cleaned_data['father_phone']
            father_email = form.cleaned_data['father_email']
            father_relationship = form.cleaned_data['father_relationship']

            father_fax = form.cleaned_data['father_fax']
            # mother
            mother_home_street = form.cleaned_data['mother_home_street']
            mother_home_town = form.cleaned_data['mother_home_town']
            mother_home_city = form.cleaned_data['mother_home_city']
            mother_home_country = form.cleaned_data['mother_home_country']
            mother_home_phone = form.cleaned_data['mother_home_phone']

            mother_work_name = form.cleaned_data['mother_work_name']
            mother_work_phone = form.cleaned_data['mother_work_phone']

            mother_first = form.cleaned_data['mother_first_name']
            mother_last = form.cleaned_data['mother_last_name']
            mother_gender = form.cleaned_data['mother_gender']
            mother_cell = form.cleaned_data['mother_phone']
            mother_email = form.cleaned_data['mother_email']
            mother_relationship = form.cleaned_data['mother_relationship']
            mother_fax = form.cleaned_data['mother_fax']
            # guardian


            if (student_first and student_last and student_gender and student_email and student_dob and
                    father_first and father_last and father_gender and father_cell and father_email and father_relationship and
                    mother_first and mother_last and mother_gender and mother_cell and mother_email and mother_relationship
                ):

                # Save Primary Guardian
                if (not father_home_street):
                    father_home_street = student_home_street
                if (not father_home_country):
                    father_home_country = student_home_country

                father_home_address = Address(
                    street=father_home_street, town=father_home_town, city=father_home_city,
                    country=father_home_country, phone=father_home_phone
                )
                father_home_address.save()
                father_home_address_id = father_home_address
                # Create Username and password
                father_username = father_first + '.' + father_last
                father_password = 'Password123'
                # Create User
                father_user = User(username=father_username, first_name=father_first, last_name=father_last,
                                   password=father_password, email=father_email)
                father_user.save()
                father_user_id = father_user
                # Assign User to Group
                parent_group = Group.objects.get(name="Parents")
                father_user.groups.add(parent_group)
                # Add User to Parent Model
                parent = Parent_Guardian(
                    gender=father_gender, personal_email=father_email, parent=father_user_id, cell_phone=father_cell,
                    personal_fax=father_fax,
                    work_phone=father_work_phone, work_name=father_work_name, relationship=father_relationship
                )
                parent.save()
                # Many to Many SaVe
                parent_address = Parent_Address(
                    address=father_home_address, parent=parent
                )
                parent_address.save()

                ###SAVE STUDEnT

                # Generate default Generic Username and Password then route to email
                student_username = student_first + '.' + student_last
                student_password = 'Password123'

                # Create User
                user = User(
                    username=student_username, first_name=student_first, last_name=student_last,
                    password=student_password,
                    email=student_email
                )
                user.save()
                user_id = user
                # Add User to Group
                student_group = Group.objects.get(name='Students')
                user.groups.add(student_group)
                # Save user Address
                student_home_address = Address(
                    street=student_home_street, town=student_home_town, city=student_home_city,
                    country=student_home_country, phone=student_home_phone
                )
                student_home_address.save()
                student_home_address_id = student_home_address
                # Add user to Student model
                student = Student(gender=student_gender, email=student_email, student=user_id, dob=student_dob,
                                  medical_conditions=student_medical,
                                  religious_belief=student_religious, allergies=student_allergies
                                  )
                student.save()

                # m2m Add parent and student
                student.parent.add(parent)
                s = Student_Address(
                    address=student_home_address, student=student
                )
                s.save()
                # Save Mother
                if (not mother_home_street):
                    mother_home_street = student_home_street
                if (not mother_home_country):
                    mother_home_country = student_home_country

                # Save mother Home address
                mother_home_address = Address(
                    street=mother_home_street, town=mother_home_town, city=mother_home_city,
                    country=mother_home_country, phone=mother_home_phone
                )
                mother_home_address.save()
                mother_home_address_id = mother_home_address

                # Generate Random Password
                mother_username = mother_first + '.' + mother_last
                mother_password = 'Password123'

                # Save User Model
                mother_user = User(username=mother_username, first_name=mother_first, last_name=mother_last,
                                   password=mother_password, email=mother_email)
                mother_user.save()
                mother_user_id = mother_user
                # Add Person to Parent Group
                parent_group = Group.objects.get(name="Parents")
                mother_user.groups.add(parent_group)
                # Add user to Parent model
                parent2 = Parent_Guardian(
                    gender=mother_gender, personal_email=mother_email, parent=mother_user_id, cell_phone=mother_cell,
                    personal_fax=mother_fax,
                    work_phone=mother_work_phone, work_name=mother_work_name, relationship=mother_relationship
                )
                parent2.save()
                ##M2M SaVE
                p = Parent_Address(
                    address=mother_home_address, parent=parent2
                )
                # m2m Add parent and student
                student.parent.add(parent2)

            # save Guardian
            else:
                print "error"
                # redirect to a new URL:
            return HttpResponseRedirect('/')
        else:
            print "form is invalid"
            print form.errors
            # If this is a GET (or any other method) create the default form.
    else:
        # set this variable to zero to say new info which is default...any other number signifies addition
        check = 0
        if (request.user.groups.filter(name='Parents')):
            # get parent object
            parent = Parent_Guardian.objects.get(parent=request.user)
            # check to see if parent already has student in school
            # get student associated with parent
            exist = Student.objects.get(parent=parent)
            print exist
            # get user id to retreive address information
            # user = Student.objects.filter(parent=parent).values_list('student')
            ##if Parent/student exist pass hidden in form address and parent info in Modelform
            if (exist):
                # get address of student
                form = StudentModelForm()
                userform = UserModelForm()
                address = exist.address.all()
                print address
                return render(request, 'primary/student_create_existing_parent.html', {
                    'userform': userform,
                    'form': form,
                    'parent': parent,
                    'address': address,
                    'check': check,
                })
            """
            if Parent has no children attaending school, then fill out student form and address form
            Set check to 1
            """
            if (not exist):
                check = 1
                form = StudentModelForm()
                userform = UserModelForm()
                addressform = AddressModelForm()
                return render(request, 'primary/student_create_existing_parent.html', {
                    'userform': userform,
                    'form': form,
                    'addressform': addressform,
                    'parent': parent,
                    'check': check,
                })
        """
        If Administrator search for existing child/and parent, or create new one 
        """
        check = 0
        if (request.user.groups.filter(name='Administrators')):
            form = CreateRegistrationForm()
    return render(request, 'create_student.html', {'form': form})


"""
"""


@login_required
def create_teacher(request):
    if request.method == "POST":
        form = CreateTeacherForm(request.POST)
        if form.is_valid():
            first = form.cleaned_data['first_name']
            print first
            last = form.cleaned_data['last_name']
            print last
            gender = form.cleaned_data['gender']
            print gender
            cell = form.cleaned_data['phone']
            print cell
            username = form.cleaned_data['username']
            print username
            password = form.cleaned_data['password']
            print password
            email = form.cleaned_data['email']
            print email
            school = form.cleaned_data['school']
            print school
            fax = form.cleaned_data['fax']
            if (first and last and gender and cell and username and password and email and school):
                print "inside"
                user = User(username=username, first_name=first, last_name=last, password=password, email=email)
                user.save()
                user_id = user
                teacher = Teacher(gender=gender, personal_email=email, school=school, teacher=user_id, cell_phone=cell,
                                  personal_fax=fax)
                teacher.save()
            else:
                print "error"
                # redirect to a new URL:
            return HttpResponseRedirect('/')

            # If this is a GET (or any other method) create the default form.
    else:

        form = CreateTeacherForm()

    return render(request, 'create_teacher.html', {'form': form})


"""
"""


@login_required
def create_school(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreateSchoolForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            street = form.cleaned_data['street']
            town = form.cleaned_data['town']
            city = form.cleaned_data['city']
            country = form.cleaned_data['country']
            phone = form.cleaned_data['phone']
            name = form.cleaned_data['name']
            principal = form.cleaned_data['principal']
            email = form.cleaned_data['email']
            type = form.cleaned_data['type']
            if (street and town and city and country and phone and name and principal and email and type):
                address = Address(street=form.cleaned_data['street'], town=form.cleaned_data['town'],
                                  city=form.cleaned_data['city'],
                                  country=form.cleaned_data['country'], phone=form.cleaned_data['phone'])
                address.save()
                address_id = address

                school = School(
                    address=address_id, name=form.cleaned_data['name'], principal=form.cleaned_data['principal'],
                    email=form.cleaned_data['email'],
                    fax=form.cleaned_data['fax'], type=form.cleaned_data['type']
                )
            school.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/')

            # If this is a GET (or any other method) create the default form.
    else:

        form = CreateSchoolForm()

    return render(request, 'create_school.html', {'form': form})
