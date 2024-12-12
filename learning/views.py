from django.shortcuts import render, redirect
from .models import Student, Teacher, Class, Attendance, Grade
from .forms import StudentForm, TeacherForm, ClassForm, AttendanceForm, GradeForm


from django.shortcuts import render

def homepage(request):
    return render(request, 'home.html')

def home(request):
    return render(request, 'home.html')

# View for student registration
def student_register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_register.html', {'form': form})

# View to list all students
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

# View for teacher registration
def teacher_register(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'teacher_register.html', {'form': form})

# View to list all teachers
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher_list.html', {'teachers': teachers})

# View for class creation
def class_create(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = ClassForm()
    return render(request, 'class_create.html', {'form': form})

# View to list all classes
def class_list(request):
    classes = Class.objects.all()
    return render(request, 'class_list.html', {'classes': classes})

# View for class enrollment (add student to class)
def enroll_student(request, student_id, class_id):
    student = Student.objects.get(id=student_id)
    class_obj = Class.objects.get(id=class_id)
    student.classes.add(class_obj)
    return redirect('student_list')

# View for attendance
def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'attendance_create.html', {'form': form})

# View for grades
def grade_create(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grade_list')
    else:
        form = GradeForm()
    return render(request, 'grade_create.html', {'form': form})
