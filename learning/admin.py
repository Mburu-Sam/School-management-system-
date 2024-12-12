from django.contrib import admin
from .models import Teacher,Class,Student,Attendance,Grade

admin.site.register(Teacher)
admin.site.register(Class)
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Grade)
