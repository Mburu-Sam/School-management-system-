from django import forms
from .models import Student, Teacher, Class, Attendance, Grade

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'classes']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'email', 'subject']

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'teacher']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'class_obj', 'date', 'present']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'class_obj', 'grade']
