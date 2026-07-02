"""
URL configuration for School project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import include, path

from learning import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admission/apply/', views.admission_apply, name='admission_apply'),
    path('signup/', views.signup_choice, name='signup_choice'),
    path('student/signup/', views.student_signup, name='student_signup'),
    path('teacher/signup/', views.teacher_signup, name='teacher_signup'),
    path('admin/signup/', views.admin_signup, name='admin_signup'),
    path('role/redirect/', views.role_redirect, name='role_redirect'),
    path('student/register/', views.student_register, name='student_register'),
    path('students/', views.student_list, name='student_list'),
    path('teacher/register/', views.teacher_register, name='teacher_register'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('class/create/', views.class_create, name='class_create'),
    path('classes/', views.class_list, name='class_list'),
    path('subject/create/', views.subject_create, name='subject_create'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('attendance/create/', views.attendance_create, name='attendance_create'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('grade/create/', views.grade_create, name='grade_create'),
    path('grades/', views.grade_list, name='grade_list'),
    path('fees/create/', views.fee_statement_create, name='fee_statement_create'),
    path('fees/', views.fee_statement_list, name='fee_statement_list'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/profile/update/', views.teacher_profile_update, name='teacher_profile_update'),
    path('teacher/subject/create/', views.teacher_subject_create, name='teacher_subject_create'),
    path('teacher/class/create/', views.teacher_class_create, name='teacher_class_create'),
    path('teacher/attendance/create/', views.teacher_attendance_create, name='teacher_attendance_create'),
    path('teacher/grade/create/', views.teacher_grade_create, name='teacher_grade_create'),
    path('teacher/assignment/create/', views.teacher_assignment_create, name='teacher_assignment_create'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/profile/update/', views.student_profile_update, name='student_profile_update'),
    path('student/transcript/download/', views.download_transcript, name='download_transcript'),
    path('student/attendance/report/download/', views.download_attendance_report, name='download_attendance_report'),
    path('student/fee/report/download/', views.download_fee_statement_report, name='download_fee_statement_report'),
    path('assignment/<int:assignment_id>/submit/', views.assignment_submit, name='assignment_submit'),
    path('enroll/student/<int:student_id>/class/<int:class_id>/', views.enroll_student, name='enroll_student'),
    path('', views.homepage, name='homepage'),
]
