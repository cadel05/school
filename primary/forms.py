from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from .models import School, Student, Address, Parent_Guardian, Teacher, Subject, Class, ClassName

import datetime, re

alnum_re = re.compile(r"^\w+$")


class SelectSubjectsForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Class.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


"""
	def __init__(self, *args, **kwargs):
		self.classes = kwargs.pop('classes')
		print self.classes
		subject_id = Class.objects.filter(id__in = self.classes).values_list('subject')
		print subject_id
		super(SelectSubjectsForm, self).__init__(*args, **kwargs)
		self.fields['subject'] = forms.ModelMultipleChoiceField(
			widget = forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
			queryset = Class.objects.filter(id__in = self.classes).values_list('subject'),
			required = True
		)
"""


class ClassNameModelForm(forms.ModelForm):
    select_subjects = forms.CharField(max_length=10, widget=forms.HiddenInput(), initial='True')

    class Meta:
        model = ClassName
        fields = ('class_name',)

        def __init__(self, *args, **kwargs):
            super(ClassNameModelForm, self).__init__(*args, **kwargs)
            self.fields['class_name'].widget.attrs['class'] = 'form-control'


class ClassNameForm(forms.Form):
    class_name = forms.ModelChoiceField(queryset=ClassName.objects.all())
    select_subjects = forms.CharField(
        max_length=10,
        widget=forms.HiddenInput(),
        initial='False',
    )

    def __init__(self, *args, **kwargs):
        super(ClassNameForm, self).__init__(*args, **kwargs)
        self.fields['class_name'].widget.attrs['class'] = 'form-control'


class ClassRegistrationForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('subject', 'class_name', 'teacher')

    def __init__(self, *args, **kwargs):
        super(ClassModelForm, self).__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs['class'] = 'form-control'
        self.fields['teacher'].widget.attrs['class'] = 'form-control'
        self.fields['class_name'].widget.attrs['class'] = 'form-control'


class StudentSearchForm(forms.Form):
    first_name = forms.CharField(
        label=_("*First Name"),
        max_length=75,
        widget=forms.TextInput(),
        required=False
    )
    last_name = forms.CharField(
        label=_("*Last Name"),
        max_length=75,
        widget=forms.TextInput(),
        required=False
    )


class ClassModelForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('subject', 'teacher', 'class_name', 'classDaysandTime', 'class_room')

    def __init__(self, *args, **kwargs):
        super(ClassModelForm, self).__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs['class'] = 'form-control'
        self.fields['teacher'].widget.attrs['class'] = 'form-control'
        self.fields['class_name'].widget.attrs['class'] = 'form-control'
        self.fields['classDaysandTime'].widget.attrs['class'] = 'form-control'
        self.fields['class_room'].widget.attrs['class'] = 'form-control'


class SubjectModelForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('subject',)

    def __init__(self, *args, **kwargs):
        super(SubjectModelForm, self).__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs['class'] = 'form-control'


class TeacherModelForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('gender', 'cell_phone', 'personal_email', 'personal_fax')

    def __init__(self, *args, **kwargs):
        super(TeacherModelForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs['class'] = 'form-control'
        self.fields['cell_phone'].widget.attrs['class'] = 'form-control'
        self.fields['personal_fax'].widget.attrs['class'] = 'form-control'
        self.fields['personal_email'].widget.attrs['class'] = 'form-control'


class SchoolModelForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ('type', 'name', 'principal', 'email', 'fax')

    def __init__(self, *args, **kwargs):
        super(SchoolModelForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['principal'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['fax'].widget.attrs['class'] = 'form-control'


class ParentModelForm(forms.ModelForm):
    class Meta:
        model = Parent_Guardian
        fields = ('gender', 'cell_phone', 'personal_fax', 'work_name', 'work_phone', 'relationship')

    def __init__(self, *args, **kwargs):
        super(ParentModelForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs['class'] = 'form-control'
        self.fields['cell_phone'].widget.attrs['class'] = 'form-control'
        self.fields['personal_fax'].widget.attrs['class'] = 'form-control'
        self.fields['work_name'].widget.attrs['class'] = 'form-control'
        self.fields['work_phone'].widget.attrs['class'] = 'form-control'
        self.fields['relationship'].widget.attrs['class'] = 'form-control'


class AddressModelForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('street', 'town', 'city', 'country', 'phone')

    def __init__(self, *args, **kwargs):
        super(AddressModelForm, self).__init__(*args, **kwargs)
        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['town'].widget.attrs['class'] = 'form-control'
        self.fields['country'].widget.attrs['class'] = 'form-control'
        self.fields['street'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'


class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'


class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('dob', 'gender', 'allergies', 'medical_conditions', 'religious_belief')

    def __init__(self, *args, **kwargs):
        super(StudentModelForm, self).__init__(*args, **kwargs)
        self.fields['dob'].widget.attrs['class'] = 'form-control'
        self.fields['gender'].widget.attrs['class'] = 'form-control'
        self.fields['allergies'].widget.attrs['class'] = 'form-control'
        self.fields['medical_conditions'].widget.attrs['class'] = 'form-control'
        self.fields['religious_belief'].widget.attrs['class'] = 'form-control'


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

TYPE = (
    ('', ''),
    ('P', 'Primary School'),
    ('S', 'Secondary School'),
)


class CreateSchoolForm(forms.Form):
    street = forms.CharField(max_length=100)
    town = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15, help_text='Please enter in the form as, 18681112222, no spaces or dashes',
                            label='School Phone')
    name = forms.CharField(max_length=100, label="School Name")
    principal = forms.CharField(max_length=100, label="Principal Full Name")
    email = forms.EmailField(label="School Email")
    fax = forms.CharField(max_length=15, required=False)
    type = forms.ChoiceField(
        label=_("*Type"),
        widget=forms.Select(),
        choices=TYPE,
        required=True
    )

    def clean_type(self):
        type = self.cleaned_data['type']

        # check to see is only alphanumberic values
        if (type == ''):
            raise forms.ValidationError("Type cannot be blank")
        return type

    def clean_street(self):
        street = self.cleaned_data['street']

        # check to see is only alphanumberic values
        if not re.match(r'^[A-Za-z0-9_]+( [A-Za-z0-9_]+)*$', street):
            raise forms.ValidationError("Street name must be alphanumberic characters only, such as 22 Me Street")
        return street

    def clean_town(self):
        town = self.cleaned_data['town']

        # check to see is only alpha values
        if not re.match(r'^[A-Za-z]+( [A-Za-z_]+)*$', town):
            raise forms.ValidationError("Town must contain only alpha characters only")
        return town

    def clean_city(self):
        city = self.cleaned_data['city']

        # check to see is only alpha values
        if not re.match(r'^[A-Za-z]+( [A-Za-z_]+)*$', city):
            raise forms.ValidationError("City must contain only alpha characters only")
        return city

    def clean_country(self):
        country = self.cleaned_data['country']

        # check to see is only alpha values
        if not re.match(r'^[A-Za-z]+( [A-Za-z_]+)*$', country):
            raise forms.ValidationError("Country must contain only alpha characters only")
        return country

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        # check to see is only numeric values
        if not re.match(r'^[0-9]+$', phone):
            raise forms.ValidationError("Phone must contain only numeric characters only, no spaces or dashes")
        return phone


GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class CreateTeacherForm(forms.Form):
    gender = forms.ChoiceField(
        label=_("*Gender"),
        widget=forms.Select(),
        choices=GENDER,
        required=True
    )

    first_name = forms.CharField(
        label=_("*First Name"),
        max_length=75,
        widget=forms.TextInput(),
        required=True
    )

    last_name = forms.CharField(
        label=_("*Last Name"),
        max_length=75,
        widget=forms.TextInput(),
        required=True
    )
    phone = forms.CharField(
        label=_("*Cell Phone pattern 1868******, no spaces or dashes allowed"),
        max_length=15,
        widget=forms.TextInput(),
        required=True
    )
    fax = forms.CharField(
        label=_("Fax pattern 1868******, no spaces or dashes allowed"),
        max_length=15,
        widget=forms.TextInput(),
        required=False
    )
    username = forms.CharField(
        label=_("*Username"),
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )
    password = forms.CharField(
        label=_(
            "*Password must be at least 8 characters and should only have alphanumeric characters and/or @#$%^&+= special characters"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_confirm = forms.CharField(
        label=_("*Password (again)"),
        widget=forms.PasswordInput(render_value=False)
    )
    email = forms.EmailField(
        label=_("*Email"),
        widget=forms.TextInput(), required=True)

    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        label=_("Select School Teacher Attends"),
        required=True
    )

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        # check to see is only numeric values
        if not re.match(r'^[0-9]+$', phone):
            raise forms.ValidationError("Phone must contain only numeric characters only, no spaces or dashes")
        return phone

    def clean_fax(self):
        fax = self.cleaned_data['fax']

        # check to see is only numeric values
        if fax and not re.match(r'^[0-9]+$', fax):
            raise forms.ValidationError("Phone must contain only numeric characters only, no spaces or dashes")
        return fax

    def clean_username(self):
        if not alnum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError(_("Usernames can only contain letters, numbers and underscores."))
        username = self.cleaned_data["username"]

        qs = User.objects.filter(username__iexact=username)
        if not qs.exists():
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("This username is already taken. Please choose another."))

    def clean_password(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
            if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', self.cleaned_data["password"]):
                return self.cleaned_data
            else:
                raise forms.ValidationError(_(
                    "You must enter at least 8 characters for a password. Only alphanumeric and @#$%^&+=, characters are allowed."))
        return self.cleaned_data["password"]


##########################################################################################################################################
# This form is used to update students profiles
#
#
#
##########################################################################################################################################		
class UpdateStudentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.first_name = kwargs.pop('user')
        super(UpdateStudentForm, self).__init__(*args, **kwargs)

    student_gender = forms.ChoiceField(
        label=_("*Student Gender"),
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=GENDER,
        required=True
    )
    student_first_name = forms.CharField(
        label=_("*Student First Name"),
        max_length=75,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    student_last_name = forms.CharField(
        label=_("*Student Last Name"),
        max_length=75,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    student_dob = forms.DateField(
        label=_("Student Date of Birth, yyyy-mm-dd"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    student_allergies = forms.CharField(
        label=_("Student Allergies"),
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    student_medical_conditions = forms.CharField(
        label=_("Student Medical Conditions"),
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    student_religious_belief = forms.CharField(
        label=_("Student Religious Belief"),
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    student_email = forms.EmailField(
        label=_("*Student Email"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )


##########################################################################################################################################
# This form is used to register students, parents and guardians
#
#
#
##########################################################################################################################################		
class CreateRegistrationForm(forms.Form):
    # Student Creation
    student_gender = forms.ChoiceField(
        label=_("*Student Gender"),
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=GENDER,
        required=True
    )

    student_first_name = forms.CharField(
        label=_("*Student First Name"),
        max_length=75,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    student_last_name = forms.CharField(
        label=_("*Student Last Name"),
        max_length=75,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    student_dob = forms.DateField(
        label=_("Student Date of Birth, yyyy-mm-dd"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    student_allergies = forms.CharField(
        label=_("Student Allergies"),
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    student_medical_conditions = forms.CharField(
        label=_("Student Medical Conditions"),
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    student_religious_belief = forms.CharField(
        label=_("Student Religious Belief"),
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    student_email = forms.EmailField(
        label=_("*Student Email"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    ##student Address
    student_home_street = forms.CharField(
        max_length=100,
        label=_("Student Home Street"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    student_home_town = forms.CharField(
        max_length=100,
        label=_("Student Home Town"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    student_home_city = forms.CharField(
        max_length=100,
        label=_("Student Home City"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    student_home_country = forms.CharField(
        max_length=100,
        label=_("Student Home Country"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    student_home_phone = forms.CharField(
        label=_("*Student Home Phone pattern 1868******, no spaces or dashes allowed"),
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    ### Create Father

    father_home_street = forms.CharField(
        help_text="Only fill this out if student lives at different address from father",
        max_length=100,
        label=_("Father Home Street"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    father_home_town = forms.CharField(
        max_length=100,
        label=_("Father Home Town"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    father_home_city = forms.CharField(
        max_length=100,
        label=_("Father Home City"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    father_home_country = forms.CharField(
        max_length=100,
        label=_("Father Home Country"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    father_home_phone = forms.CharField(
        label=_("*Father Home Phone pattern 1868******, no spaces or dashes allowed"),
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    father_work_name = forms.CharField(
        max_length=150,
        label=_("Father Organization Name"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    father_work_phone = forms.CharField(
        label=_("*Father Work Phone pattern 1868******, no spaces or dashes allowed"),
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    father_gender = forms.ChoiceField(
        label=_("*Father Gender"),
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=GENDER,
        required=True
    )

    father_first_name = forms.CharField(
        label=_("*Father First Name"),
        max_length=75,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    father_last_name = forms.CharField(
        label=_("*Father Last Name"),
        max_length=75,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    father_phone = forms.CharField(
        label=_("*Father Cell Phone pattern 1868******, no spaces or dashes allowed"),
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    father_fax = forms.CharField(
        label=_("Father Fax pattern 1868******, no spaces or dashes allowed"),
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    father_email = forms.EmailField(
        label=_("*Father Email"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    father_relationship = forms.ChoiceField(
        label=_("*Guardian Relationship"),
        choices=RELATIONSHIP,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    def clean_student_homestreet(self):
        student_home_street = self.cleaned_data['student_home_street']

        # check to see is only alphanumberic values
        if not re.match(r'^[A-Za-z0-9_]+( [A-Za-z0-9_]+)*$', student_home_street):
            raise forms.ValidationError("Street name must be alphanumberic characters only, such as 22 Me Street")
        return student_home_street

    def clean_student_hometown(self):
        student_home_town = self.cleaned_data['student_home_town']

        # check to see is only alpha values
        if not re.match(r'^[A-Za-z]+( [A-Za-z_]+)*$', student_home_town):
            raise forms.ValidationError("Town must contain only alpha characters only")
        return student_home_town

    def clean_student_homecity(self):
        student_home_city = self.cleaned_data['student_home_city']

        # check to see is only alpha values
        if not re.match(r'^[A-Za-z]+( [A-Za-z_]+)*$', student_home_city):
            raise forms.ValidationError("City must contain only alpha characters only")
        return student_home_city

    def clean_student_homecountry(self):
        student_home_country = self.cleaned_data['student_home_country']

        # check to see is only alpha values
        if not re.match(r'^[A-Za-z]+( [A-Za-z_]+)*$', student_home_country):
            raise forms.ValidationError("Country must contain only alpha characters only")
        return student_home_country

    def clean_student_homephone(self):
        student_home_phone = self.cleaned_data['student_home_phone']

        # check to see is only numeric values
        if not re.match(r'^[0-9]+$', student_home_phone):
            raise forms.ValidationError("Phone must contain only numeric characters only, no spaces or dashes")
        return student_home_phone

    ##father validation
    def clean_student_homestreet(self):
        father_home_street = self.cleaned_data['father_home_street']

        # check to see is only alphanumberic values
        if not re.match(r'^[A-Za-z0-9_]+( [A-Za-z0-9_]+)*$', father_home_street):
            raise forms.ValidationError("Street name must be alphanumberic characters only, such as 22 Me Street")
        return father_home_street

    def clean_student_hometown(self):
        father_home_town = self.cleaned_data['father_home_town']

        # check to see is only alpha values
        if not re.match(r'^[A-Za-z]+( [A-Za-z_]+)*$', father_home_town):
            raise forms.ValidationError("Town must contain only alpha characters only")
        return father_home_town

    def clean_homecity(self):
        father_home_city = self.cleaned_data['father_home_city']

        # check to see is only alpha values
        if not re.match(r'^[A-Za-z]+( [A-Za-z_]+)*$', father_home_city):
            raise forms.ValidationError("City must contain only alpha characters only")
        return father_home_city

    def clean_homecountry(self):
        father_home_country = self.cleaned_data['father_home_country']

        # check to see is only alpha values
        if not re.match(r'^[A-Za-z]+( [A-Za-z_]+)*$', father_home_country):
            raise forms.ValidationError("Country must contain only alpha characters only")
        return father_home_country

    def clean_homephone(self):
        father_home_phone = self.cleaned_data['father_home_phone']

        # check to see is only numeric values
        if not re.match(r'^[0-9]+$', father_home_phone):
            raise forms.ValidationError("Phone must contain only numeric characters only, no spaces or dashes")
        return father_home_phone

    def clean_workname(self):
        father_work_name = self.cleaned_data['father_work_name']

        # check to see is only alphanumberic values
        if not re.match(r'^[A-Za-z0-9_]+( [A-Za-z0-9_]+)*$', father_work_street):
            raise forms.ValidationError("Street name must be alphanumberic characters only, such as 22 Me Street")
        return father_work_name

    def clean_workphone(self):
        father_home_phone = self.cleaned_data['father_home_phone']

        # check to see is only numeric values
        if not re.match(r'^[0-9]+$', father_home_phone):
            raise forms.ValidationError("Phone must contain only numeric characters only, no spaces or dashes")
        return father_home_phone

    def clean_phone(self):
        father_phone = self.cleaned_data['father_phone']

        # check to see is only numeric values
        if not re.match(r'^[0-9]+$', father_phone):
            raise forms.ValidationError("Phone must contain only numeric characters only, no spaces or dashes")
        return father_phone

    def clean_fax(self):
        father_fax = self.cleaned_data['father_fax']

        # check to see is only numeric values
        if not re.match(r'^[0-9]+$', father_fax):
            raise forms.ValidationError("Phone must contain only numeric characters only, no spaces or dashes")
        return father_fax

    ### Create Mother

    mother_home_street = forms.CharField(
        max_length=100,
        label=_("Mother Home Street"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    mother_home_town = forms.CharField(
        max_length=100,
        label=_("Mother Home Town"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    mother_home_city = forms.CharField(
        max_length=100,
        label=_("Mother Home City"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    mother_home_country = forms.CharField(
        max_length=100,
        label=_("Mother Home Country"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    mother_home_phone = forms.CharField(
        label=_("*Mother Home Phone pattern 1868******, no spaces or dashes allowed"),
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    mother_work_name = forms.CharField(
        max_length=150,
        label=_("Mother Organization Name"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    mother_work_phone = forms.CharField(
        label=_("*Mother Work Phone pattern 1868******, no spaces or dashes allowed"),
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    mother_relationship = forms.ChoiceField(
        label=_("*Guardian Relationship"),
        choices=RELATIONSHIP,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    mother_gender = forms.ChoiceField(
        label=_("*Mother Gender"),
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=GENDER,
        required=True
    )

    mother_first_name = forms.CharField(
        label=_("*Mother First Name"),
        max_length=75,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    mother_last_name = forms.CharField(
        label=_("*Mother Last Name"),
        max_length=75,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    mother_phone = forms.CharField(
        label=_("*Mother Cell Phone pattern 1868******, no spaces or dashes allowed"),
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    mother_fax = forms.CharField(
        label=_("Mother Fax pattern 1868******, no spaces or dashes allowed"),
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    mother_email = forms.EmailField(
        label=_("*Mother Email"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    def clean_mother_homestreet(self):
        mother_home_street = self.cleaned_data['mother_home_street']

        # check to see is only alphanumberic values
        if not re.match(r'^[A-Za-z0-9_]+( [A-Za-z0-9_]+)*$', mother_home_street):
            raise forms.ValidationError("Street name must be alphanumberic characters only, such as 22 Me Street")
        return mother_home_street

    def clean_mother_hometown(self):
        father_home_town = self.cleaned_data['mother_home_town']

        # check to see is only alpha values
        if not re.match(r'^[A-Za-z]+( [A-Za-z_]+)*$', father_home_town):
            raise forms.ValidationError("Town must contain only alpha characters only")
        return father_home_town

    def clean_mother_homecity(self):
        mother_home_city = self.cleaned_data['mother_home_city']

        # check to see is only alpha values
        if not re.match(r'^[A-Za-z]+( [A-Za-z_]+)*$', mother_home_city):
            raise forms.ValidationError("City must contain only alpha characters only")
        return mother_home_city

    def clean_mother_homecountry(self):
        mother_home_country = self.cleaned_data['mother_home_country']

        # check to see is only alpha values
        if not re.match(r'^[A-Za-z]+( [A-Za-z_]+)*$', mother_home_country):
            raise forms.ValidationError("Country must contain only alpha characters only")
        return mother_home_country

    def clean_mother_homephone(self):
        mother_home_phone = self.cleaned_data['mother_home_phone']

        # check to see is only numeric values
        if not re.match(r'^[0-9]+$', mother_home_phone):
            raise forms.ValidationError("Phone must contain only numeric characters only, no spaces or dashes")
        return mother_home_phone

    def clean_mother_workname(self):
        mother_work_name = self.cleaned_data['mother_work_name']

        # check to see is only alphanumberic values
        if not re.match(r'^[A-Za-z0-9_]+( [A-Za-z0-9_]+)*$', mother_work_street):
            raise forms.ValidationError("Street name must be alphanumberic characters only, such as 22 Me Street")
        return mother_work_name

    def clean_mother_workphone(self):
        mother_home_phone = self.cleaned_data['mother_home_phone']

        # check to see is only numeric values
        if not re.match(r'^[0-9]+$', mother_home_phone):
            raise forms.ValidationError("Phone must contain only numeric characters only, no spaces or dashes")
        return mother_home_phone

    def clean_mother_phone(self):
        mother_phone = self.cleaned_data['mother_phone']

        # check to see is only numeric values
        if not re.match(r'^[0-9]+$', mother_phone):
            raise forms.ValidationError("Phone must contain only numeric characters only, no spaces or dashes")
        return mother_phone


### Create Guardian


## Create Parents
class CreateParentForm(forms.Form):
    home_street = forms.CharField(
        max_length=100,
        label=_("Home Street"),
        widget=forms.TextInput(),
        required=True
    )

    home_town = forms.CharField(
        max_length=100,
        label=_("Home Town"),
        widget=forms.TextInput(),
        required=True
    )

    home_city = forms.CharField(
        max_length=100,
        label=_("Home City"),
        widget=forms.TextInput(),
        required=True
    )

    home_country = forms.CharField(
        max_length=100,
        label=_("Home Country"),
        widget=forms.TextInput(),
        required=True
    )

    home_phone = forms.CharField(
        label=_("*Home Phone pattern 1868******, no spaces or dashes allowed"),
        max_length=15,
        widget=forms.TextInput(),
        required=True
    )

    work_name = forms.CharField(
        max_length=150,
        label=_("Organization Name"),
        widget=forms.TextInput(),
        required=True
    )

    work_phone = forms.CharField(
        label=_("*Work Phone pattern 1868******, no spaces or dashes allowed"),
        max_length=15,
        widget=forms.TextInput(),
        required=True
    )

    gender = forms.ChoiceField(
        label=_("*Gender"),
        widget=forms.Select(),
        choices=GENDER,
        required=True
    )

    first_name = forms.CharField(
        label=_("*First Name"),
        max_length=75,
        widget=forms.TextInput(),
        required=True
    )

    last_name = forms.CharField(
        label=_("*Last Name"),
        max_length=75,
        widget=forms.TextInput(),
        required=True
    )
    phone = forms.CharField(
        label=_("*Cell Phone pattern 1868******, no spaces or dashes allowed"),
        max_length=15,
        widget=forms.TextInput(),
        required=True
    )
    fax = forms.CharField(
        label=_("Fax pattern 1868******, no spaces or dashes allowed"),
        max_length=15,
        widget=forms.TextInput(),
        required=False
    )
    email = forms.EmailField(
        label=_("*Email"),
        widget=forms.TextInput(), required=True)

    def clean_homestreet(self):
        home_street = self.cleaned_data['home_street']

        # check to see is only alphanumberic values
        if not re.match(r'^[A-Za-z0-9_]+( [A-Za-z0-9_]+)*$', home_street):
            raise forms.ValidationError("Street name must be alphanumberic characters only, such as 22 Me Street")
        return home_street

    def clean_hometown(self):
        home_town = self.cleaned_data['home_town']

        # check to see is only alpha values
        if not re.match(r'^[A-Za-z]+( [A-Za-z_]+)*$', home_town):
            raise forms.ValidationError("Town must contain only alpha characters only")
        return home_town

    def clean_homecity(self):
        home_city = self.cleaned_data['home_city']

        # check to see is only alpha values
        if not re.match(r'^[A-Za-z]+( [A-Za-z_]+)*$', home_city):
            raise forms.ValidationError("City must contain only alpha characters only")
        return home_city

    def clean_homecountry(self):
        home_country = self.cleaned_data['home_country']

        # check to see is only alpha values
        if not re.match(r'^[A-Za-z]+( [A-Za-z_]+)*$', home_country):
            raise forms.ValidationError("Country must contain only alpha characters only")
        return home_country

    def clean_homephone(self):
        home_phone = self.cleaned_data['home_phone']

        # check to see is only numeric values
        if not re.match(r'^[0-9]+$', phone):
            raise forms.ValidationError("Phone must contain only numeric characters only, no spaces or dashes")
        return home_phone

    def clean_workname(self):
        work_name = self.cleaned_data['work_name']

        # check to see is only alphanumberic values
        if not re.match(r'^[A-Za-z0-9_]+( [A-Za-z0-9_]+)*$', work_street):
            raise forms.ValidationError("Street name must be alphanumberic characters only, such as 22 Me Street")
        return work_name

    def clean_workphone(self):
        home_phone = self.cleaned_data['work_phone']

        # check to see is only numeric values
        if not re.match(r'^[0-9]+$', phone):
            raise forms.ValidationError("Phone must contain only numeric characters only, no spaces or dashes")
        return work_phone

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        # check to see is only numeric values
        if not re.match(r'^[0-9]+$', phone):
            raise forms.ValidationError("Phone must contain only numeric characters only, no spaces or dashes")
        return phone

    def clean_fax(self):
        fax = self.cleaned_data['fax']

        # check to see is only numeric values
        if fax and not re.match(r'^[0-9]+$', fax):
            raise forms.ValidationError("Phone must contain only numeric characters only, no spaces or dashes")
        return fax
