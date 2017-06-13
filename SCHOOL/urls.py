"""SCHOOL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from primary import views

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="index.html"), name="index"),

    url(r'^school/create/$', views.create_school, name='create_school'),
    url(r'^school/update/(?P<pk>[0-9]+)/$', views.SchoolUpdateView.as_view(), name='update_school'),
    url(r'^school/list/$', views.SchoolListView.as_view(), name='list_school'),
    url(r'^school/update/address/(?P<address_id>[0-9]+)/(?P<school_id>[0-9]+)/$', views.school_address_update,
        name="school_address_update"),

    url(r'^school/subject/list/$', views.SubjectListView.as_view(), name='list_subject'),
    url(r'^school/subject/create/$', views.SubjectCreateView.as_view(), name='create_subject'),
    url(r'^school/subject/update/(?P<pk>[0-9]+)/$', views.SubjectUpdateView.as_view(), name='update_subject'),

    url(r'^class/class/create/$', views.ClassCreateView.as_view(), name='create_class'),
    url(r'^class/class/list/$', views.ClassListView.as_view(), name='list_class'),
    url(r'^class/class/update/(?P<pk>[0-9]+)/$', views.ClassUpdateView.as_view(), name='update_class'),

    # url(r'^class/student/subject/register/$', views.student_subject_register, name='select_subjects_save'),

    url(r'^class/student/search/$', views.searchStudent, name='search_student'),
    url(r'^class/student/register/(?P<student_id>[0-9]+)/(?P<user_id>[0-9]+)/$', views.classRegistration,
        name='register_class'),

    url(r'^school/create/teacher/$', views.create_teacher, name='create_teacher'),
    url(r'^school/create/parent/$', views.create_parent, name='create_parent'),
    url(r'^school/create/student/$', views.create_student, name='create_student'),
    # url(r'^school/update/student/(?P<pk>\d+)/$', views.StudentUpdate.as_view(), name='update_student'),
    url(r'^school/view/student/profile/$', views.profile_student, name='profile_student'),

    url(r'^school/view/student/detail/(?P<student_id>[0-9]+)/$', views.profile_student_details,
        name="profile_student_details"),
    url(r'^school/view/parent/detail/(?P<parent_id>[0-9]+)/$', views.profile_parent_details,
        name="profile_parent_details"),

    url(r'^school/view/student/update/(?P<student_id>[0-9]+)/$', views.profile_student_update,
        name="profile_student_update"),
    url(r'^school/view/parent/update/(?P<parent_id>[0-9]+)/$', views.profile_parent_update,
        name="profile_parent_update"),
    url(r'^school/view/teacher/update/(?P<teacher_id>[0-9]+)/$', views.profile_teacher_update,
        name="profile_teacher_update"),
    url(r'^teacher/list/$', views.TeacherListView.as_view(), name='list_teacher'),

    url(r'^school/view/parent/update/address/(?P<parent_id>[0-9]+)/(?P<address_id>[0-9]+)$',
        views.profile_parent_address_update, name="profile_parent_address_update"),
    url(r'^school/view/student/update/address/(?P<student_id>[0-9]+)/(?P<address_id>[0-9]+)$',
        views.profile_student_address_update, name="profile_student_address_update"),
    url(r'^school/view/student/$', views.StudentListView.as_view(), name='student'),
    url(r'^admin/', admin.site.urls),
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url('^accounts/', include('django.contrib.auth.urls')),
]
